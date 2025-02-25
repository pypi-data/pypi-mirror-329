import asyncio
import base64
import hashlib
import hmac
import logging
import shutil
import time
import xml.etree.ElementTree as ET
from collections.abc import Awaitable, Callable
from datetime import datetime, timezone
from enum import Enum
from sqlite3 import Connection
from typing import Any, Never, cast

from aiohttp import web

from raphson_mp import (
    activity,
    auth,
    db,
    i18n,
    metadata,
    music,
    scanner,
    search,
    settings,
    util,
)
from raphson_mp.auth import User
from raphson_mp.common.image import ImageFormat, ImageQuality
from raphson_mp.common.lyrics import PlainLyrics, TimeSyncedLyrics, ensure_plain
from raphson_mp.common.track import AudioFormat
from raphson_mp.decorators import Route, simple_route
from raphson_mp.music import Playlist, Track

# https://www.subsonic.org/pages/api.jsprequest.config_dict[CONN]
# https://opensubsonic.netlify.app/docs/

_LOGGER = logging.getLogger(__name__)


class SubsonicError(Enum):
    GENERIC = 0
    PARAMETER_MISSING = 10
    CLIENT_INCOMPATIBLE = 20
    SERVER_INCOMPATIBLE = 30
    WRONG_USERNAME_OR_PASSWORD = 40
    TOKEN_AUTHENTICATION_NOT_SUPPORTED = 41
    AUTHENTICATION_MECHANISM_NOT_SUPPORTED = 42
    MULTIPLE_AUTHENTICATION = 43
    INVALID_API_KEY = 44
    USER_NOT_AUTHORIZED = 50
    TRIAL_PERIOD_OVER = 60
    REQUESTED_DATA_NOT_FOUND = 70


class SubsonicStatus(Enum):
    OK = "ok"
    FAILED = "failed"


def dict_to_xml(root: ET.Element, data: dict[str, Any]):
    for key, value in data.items():
        if type(value) == str:
            root.set(key, value)
        elif type(value) == int:
            root.set(key, str(value))
        elif type(value) == bool:
            root.set(key, "true" if value else "false")
        elif type(value) == dict:
            subtree = ET.Element(key)
            dict_to_xml(subtree, cast(dict[str, Any], value))
            root.append(subtree)
        elif type(value) == list:
            for item in cast(list[Any], value):
                if type(item) == dict:
                    subtree = ET.Element(key)
                    dict_to_xml(subtree, cast(dict[str, Any], item))
                    root.append(subtree)
                else:
                    _LOGGER.warning("cannot convert list item to xml: %s", item)
                    continue


def response(request: web.Request, data: dict[str, Any] | None = None, status: SubsonicStatus = SubsonicStatus.OK):
    if data is None:
        data = {}

    data: dict[str, Any] = {
        "subsonic-response": {
            "status": status.value,
            "version": "1.16.1",
            "type": "Raphson",
            "serverVersion": settings.server_version,
            "openSubsonic": True,
            **data,
        }
    }

    if "f" not in request.query or request.query["f"] == "xml":
        root = ET.Element("subsonic-response")
        dict_to_xml(root, data["subsonic-response"])
        xml = ET.tostring(root)
        return web.Response(body=xml, content_type="application/xml")
    elif "f" in request.query and request.query["f"] == "json":
        return web.json_response(data)

    raise ValueError()


def error(request: web.Request, error: SubsonicError) -> Never:
    resp = response(request, {"error": {"code": error.value}}, status=SubsonicStatus.FAILED)
    assert resp.body
    raise web.HTTPOk(text=resp.body.decode(), content_type=resp.content_type)


async def verify_auth(request: web.Request) -> User:
    with db.connect(read_only=True) as conn:
        if "u" in request.query and "p" in request.query:
            username = request.query["u"]
            password = request.query["p"]  # password is actually music player session token
            if password.startswith("enc:"):  # some clients send hex encoded password
                password = bytes.fromhex(password[4:]).decode()
            session = await auth.verify_token(request, password)
            if session is None:
                error(request, SubsonicError.WRONG_USERNAME_OR_PASSWORD)
            user = User.get(conn, session=session)
            assert user.username == username
            return user
        elif "t" in request.query:
            username = request.query["u"]
            hashed_token = request.query["t"]
            salt = request.query["s"]
            for (token,) in conn.execute(
                "SELECT token FROM session JOIN user ON user.id = user WHERE username = ?", (username,)
            ):
                if not hmac.compare_digest(hashlib.md5((token + salt).encode()).hexdigest(), hashed_token):
                    continue
                session = await auth.verify_token(request, token)
                if not session:
                    continue
                user = User.get(conn, session=session)
                return user
            _LOGGER.warning("no matching session token found")
            error(request, SubsonicError.WRONG_USERNAME_OR_PASSWORD)
        else:
            error(request, SubsonicError.AUTHENTICATION_MECHANISM_NOT_SUPPORTED)


SubsonicHandler = Callable[[web.Request, Connection, User], Awaitable[web.StreamResponse]]


def subsonic_route(path: str) -> Callable[[SubsonicHandler], Route]:
    def decorator(handler: SubsonicHandler) -> Route:
        async def wrapper(request: web.Request) -> web.StreamResponse:
            with db.connect(read_only=True) as conn:
                user = await verify_auth(request)
                return await handler(request, conn, user)

        return Route(
            [
                web.route("GET", path, wrapper),
                # some clients append .view to the API method
                web.route("GET", path + ".view", wrapper),
            ]
        )

    return decorator


URLSAFE_ENCODE = bytes.maketrans(b"+/=", b"-_.")
URLSAFE_DECODE = bytes.maketrans(b"-_.", b"+/=")


def to_id(name: str) -> str:
    # Some Subsonic applications don't correctly url-encode the ID, so translate it to urlsafe base64
    assert name
    return base64.b64encode(name.encode()).decode().translate(URLSAFE_ENCODE)


def from_id(b64: str) -> str:
    assert b64
    return base64.b64decode(b64.encode().translate(URLSAFE_DECODE)).decode()


def SubsonicChild(conn: Connection, track: Track, detailed: bool = False) -> dict[str, Any]:
    # https://opensubsonic.netlify.app/docs/responses/child/
    play_count = conn.execute("SELECT COUNT(*) FROM history WHERE track=?", (track.relpath,)).fetchone()[0]
    meta = track.metadata()
    data: dict[str, str | int | bool] = {
        "id": to_id(track.relpath),
        "parent": track.playlist,
        "isDir": False,
        "title": meta.title if meta.title else meta.display_title(),
        "coverArt": to_id(track.relpath),
        "duration": track.duration,
    }

    if primary_artist := meta.primary_artist():
        data["artist"] = primary_artist
        data["artistId"] = to_id(primary_artist)
        data["displayArtist"] = primary_artist

    if meta.album:
        data["album"] = meta.album
        data["albumId"] = to_id(meta.album)

    # TODO genres
    # TODO artists

    if detailed:
        data["parent"] = track.playlist
        data["suffix"] = track.relpath.split(".")[-1]
        data["transcodedContentType"] = AudioFormat.WEBM_OPUS_HIGH.content_type
        data["path"] = track.relpath
        data["mediaType"] = "song"
        data["playCount"] = play_count
        if meta.year:
            data["year"] = meta.year
        if meta.tags:
            data["genre"] = meta.tags[0]
        data["created"] = track.ctime_dt.isoformat()

    return data


def SubsonicArrayChild(conn: Connection, count: int, offset: int):
    return [
        SubsonicChild(conn, Track.by_relpath(conn, relpath))
        for relpath, in conn.execute(f"SELECT path FROM track LIMIT {count} OFFSET {offset}").fetchall()
    ]


# https://opensubsonic.netlify.app/docs/responses/albumid3/
def SubsonicAlbumID3(conn: Connection, album: str, artist: str | None) -> dict[str, Any]:
    arbitrary_path, artist, total_count, total_duration, created, year = conn.execute(
        """
        SELECT path, album_artist, COUNT(*), SUM(duration), MIN(ctime), MIN(year)
        FROM track
        WHERE album = ?
        """,
        (album,),
    ).fetchone()
    # TODO use album artist for matching

    data = {
        "id": to_id(album),
        "name": album,
        "coverArt": to_id(arbitrary_path),
        "songCount": total_count,
        "duration": total_duration,
        "year": year,
        # genre TODO
        # genres TODO
        # displayArtist TODO
        "sortName": album,
        "isCompilation": metadata.ignore_album(album),
    }

    if created:
        data["created"] = datetime.fromtimestamp(created, tz=timezone.utc).isoformat()

    if artist:
        data["artist"] = artist
        data["artistId"] = artist

    return data


def SubsonicAlbumID3WithSongs(conn: Connection, album: str, artist: str | None) -> dict[str, Any]:
    # https://opensubsonic.netlify.app/docs/responses/albumid3withsongs/

    query = "SELECT path FROM track WHERE album = ?"
    params: list[str] = [album]

    if artist:
        query += " AND album_artist = ?"
        params.append(artist)

    data = SubsonicAlbumID3(conn, album, artist)
    data["song"] = [
        SubsonicChild(conn, Track.by_relpath(conn, path), detailed=True) for path, in conn.execute(query, params)
    ]
    return data


# def SubsonicArtistID3(request: web.Request, conn: Connection, name: str):
#     # https://opensubsonic.netlify.app/docs/responses/artistid3/
#     arbitrary_track = conn.execute("SELECT track FROM track_artist WHERE artist = ? LIMIT 1", (name,)).fetchone()[0]
#     album_count = conn.execute(
#         "SELECT COUNT(DISTINCT album) FROM track JOIN track_artist ON path = track WHERE artist = ?", (name,)
#     ).fetchone()[0]
#     request.url.query
#     return {
#         "id": to_id(name),
#         "name": name,
#         "coverArt": to_id(arbitrary_track),
#         "artistImageUrl": build_coverart_url(request, to_id(arbitrary_track)),
#         "albumCount": album_count,
#     }


def SubsonicArrayArtistID3(conn: Connection, count: int, offset: int):
    return [
        {
            "id": to_id(artist),
            "name": artist,
        }
        for artist, in conn.execute(
            f"""
            SELECT DISTINCT artist
            FROM track_artist
            LIMIT {count} OFFSET {offset}
            """
        )
    ]


def SubsonicArtist(conn: Connection, name: str):
    # https://opensubsonic.netlify.app/docs/responses/artist/
    return {
        "id": to_id(name),
        "name": name,
        "album": [
            SubsonicAlbumID3(conn, album, album_artist)
            for album, album_artist in conn.execute(
                """
                SELECT album, album_artist
                FROM track JOIN track_artist ON path = track
                WHERE artist = ? AND album IS NOT NULL
                GROUP BY album
                """,
                (name,),
            )
        ],
    }


def SubsonicPlaylist(conn: Connection, name: str, include_tracks: bool = False) -> dict[str, Any]:
    # https://opensubsonic.netlify.app/docs/responses/playlist
    playlist = Playlist.by_name(conn, name)
    data: dict[str, Any] = {
        "id": to_id(name),
        "name": name,
        "songCount": playlist.track_count,
        "duration": playlist.duration,
        "created": datetime.now().isoformat(),  # TODO
        "changed": playlist.changed.isoformat(),
    }

    if include_tracks:
        data["entry"] = [SubsonicChild(conn, track) for track in playlist.tracks()]

    return data


def SubsonicArrayPlaylist(conn: Connection, user: User) -> dict[str, Any]:
    # https://opensubsonic.netlify.app/docs/responses/playlists

    return {
        "playlist": [
            SubsonicPlaylist(conn, name)
            for name, in conn.execute("SELECT playlist FROM user_playlist_favorite WHERE user = ?", (user.user_id,))
        ]
    }


def SubsonicGenre(conn: Connection, tag: str):
    song_count, album_count = conn.execute(
        "SELECT COUNT(DISTINCT path), COUNT(distinct ALBUM) FROM track JOIN track_tag ON path = track WHERE tag = ?",
        (tag,),
    )
    return {
        "value": tag,
        "songCount": song_count,
        "albumCount": album_count,
    }


def SubsonicArrayGenre(conn: Connection):
    return [
        {
            "value": tag,
            "songCount": song_count,
            "albumCount": album_count,
        }
        for tag, song_count, album_count in conn.execute(
            """
            SELECT tag, COUNT(DISTINCT path), COUNT(distinct ALBUM)
            FROM track JOIN track_tag ON path = track
            GROUP BY tag
            """
        )
    ]


@simple_route("/getOpenSubsonicExtensions", "/getOpenSubsonicExtensions.view")  # must be publicly accessible
async def getOpenSubsonicExtensions(request: web.Request):
    # https://opensubsonic.netlify.app/docs/endpoints/getopensubsonicextensions/
    data = {
        "openSubsonicExtensions": [
            {
                "name": "songLyrics",
                "versions": [1],
            },
        ],
    }
    return response(request, data)


@subsonic_route("/ping")
async def ping(request: web.Request, _conn: Connection, _user: User):
    return response(request, {})


@subsonic_route("/getArtists")
async def getArtists(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getartists/
    data: Any = {"artists": {"ignoredArticles": "The An A Die Das Ein Eine Les Le La", "index": []}}

    indices: Any = {}
    for (artist,) in conn.execute("SELECT DISTINCT artist FROM track_artist"):
        index = artist[:1].lower()
        if index not in indices:
            indices[index] = {"name": index, "artist": []}

        indices[index]["artist"].append({"id": to_id(artist), "name": artist})

    for _index, value in indices.items():
        data["artists"]["index"].append(value)

    return response(request, data)


@subsonic_route("/getArtist")
async def getArtist(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getartist/

    # Tempo sometimes issues getArtist requests without id= specified (must be a bug?)
    if "id" not in request.query:
        return response(request, data={}, status=SubsonicStatus.FAILED)

    artist = from_id(request.query["id"])
    return response(request, {"artist": SubsonicArtist(conn, artist)})


@subsonic_route("/getAlbumList2")
async def getAlbumList2(request: web.Request, conn: Connection, user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getalbumlist2/
    t = request.query["type"]

    query = "SELECT album, album_artist"
    params: list[str | int] = []

    if t == "random":
        query += """
        FROM track
        WHERE album IS NOT NULL
        GROUP BY album
        ORDER BY RANDOM()
        """
    elif t == "newest":
        query += """
        FROM track
        WHERE album IS NOT NULL
        GROUP BY album
        ORDER BY ctime DESC
        """
    elif t == "highest":
        # not supported, return an empty list
        query += "FROM track WHERE 0"
    elif t == "frequent":
        query += """
        FROM track JOIN history ON track.path = history.track
        WHERE album IS NOT NULL AND user = ?
        GROUP BY album
        ORDER BY COUNT(*) DESC
        """
        params.append(user.user_id)
    elif t == "recent":
        query += """
        FROM track JOIN history ON track.path = history.track
        WHERE album IS NOT NULL AND user = ?
        GROUP BY album
        ORDER BY timestamp DESC
        """
        params.append(user.user_id)
    elif t == "byYear":
        query += """
        FROM track
        WHERE album IS NOT NULL AND year >= ? AND year <= ?
        GROUP BY album
        ORDER BY year
        """
        params.extend((int(request.query["fromYear"]), int(request.query["toYear"])))
    elif t == "byGenre":
        query += """
        FROM track
        JOIN track_tag ON path = track
        WHERE album IS NOT NULL AND tag = ?
        GROUP BY album
        """
        params.append(request.query["genre"])
    elif t == "alphabeticalByName":
        query += """
        FROM track
        WHERE album IS NOT NULL
        GROUP BY album
        ORDER BY album ASC
        """
    elif t == "alphabeticalByArtist":
        query += """
        FROM track
        WHERE album IS NOT NULL
        GROUP BY album
        ORDER BY album_artist ASC
        """
    else:
        raise ValueError(t)

    size = int(request.query.get("size", 10))
    offset = int(request.query.get("offset", 0))
    query += f"LIMIT {size} OFFSET {offset}"

    data: Any = {
        "albumList2": {
            "album": [
                SubsonicAlbumID3(conn, album, album_artist) for album, album_artist in conn.execute(query, params)
            ]
        }
    }

    return response(request, data)


@subsonic_route("/getCoverArt")
async def getCoverArt(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getcoverart/
    cover_id = from_id(request.query["id"])
    track = Track.by_relpath(conn, cover_id)
    if not track:
        return response(request, {}, status=SubsonicStatus.FAILED)

    cover_bytes = await track.get_cover(False, ImageQuality.HIGH, ImageFormat.JPEG)
    return web.Response(body=cover_bytes, content_type="image/jpeg")


@subsonic_route("/getAlbum")
async def getAlbum(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getalbum/
    # TODO album id should be name + separator + artist instead of just the album name
    album = from_id(request.query["id"])
    return response(request, {"album": SubsonicAlbumID3WithSongs(conn, album, None)})


@subsonic_route("/getSong")
async def getSong(request: web.Request, conn: Connection, _user: User):
    relpath = from_id(request.query["id"])
    track = Track.by_relpath(conn, relpath)
    return response(request, data={"song": SubsonicChild(conn, track, detailed=True)})


@subsonic_route("/stream")
async def stream(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/stream/
    track = Track.by_relpath(conn, from_id(request.query["id"]))
    return await track.transcoded_audio(AudioFormat.WEBM_OPUS_HIGH)


@subsonic_route("/download")
async def download(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/download/
    # supposed to return original audio file without transcoding, but we return the transcoded file anyway
    # opus is good quality and storage is precious
    track = Track.by_relpath(conn, from_id(request.query["id"]))
    return await track.transcoded_audio(AudioFormat.WEBM_OPUS_HIGH)


@subsonic_route("/getLyrics")
async def getLyrics(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getlyrics/
    if "artist" not in request.query or "title" not in request.query:
        _LOGGER.warning("received getLyrics request without title or without artist")
        return response(request, status=SubsonicStatus.FAILED)

    artist = request.query["artist"]
    title = request.query["title"]

    lyrics: PlainLyrics | None = None
    track: Track | None = None

    for (relpath,) in conn.execute(
        """
        SELECT path
        FROM track JOIN track_artist ON path = track
        WHERE title = ? AND artist = ?
        """,
        (title, artist),
    ).fetchall():
        track = Track.by_relpath(conn, relpath)
        _LOGGER.info("found track for lyrics: %s", relpath)
        lyrics = ensure_plain(await track.lyrics())
        if lyrics is not None:
            break

    if lyrics is None:
        lyrics = PlainLyrics("N/A", i18n.gettext("No lyrics found"))

    data = {
        "lyrics": {
            "value": lyrics.text,
        }
    }

    if track:
        meta = track.metadata()
        artist = meta.primary_artist()
        if artist:
            data["lyrics"]["artist"] = artist
        if meta.title:
            data["lyrics"]["title"] = meta.title

    return response(request, data)

    _LOGGER.info("no lyrics")
    return response(request, status=SubsonicStatus.FAILED)


@subsonic_route("/getLyricsBySongId")
async def getLyricsBySongId(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getlyricsbysongid/
    track = Track.by_relpath(conn, from_id(request.query["id"]))
    meta = track.metadata()
    lyrics = await track.lyrics()

    lines: list[Any] = []
    if isinstance(lyrics, TimeSyncedLyrics):
        for line in lyrics.text:
            lines.append({"start": int(line.start_time * 1000), "value": line.text})
    elif isinstance(lyrics, PlainLyrics):
        for line in lyrics.text.splitlines():
            lines.append({"value": line})
    else:
        # no lyrics
        return response(request, {"lyricsList": {"structuredLyrics": []}})

    data = {
        "lyricsList": {
            "structuredLyrics": [
                {
                    "lang": "und",
                    "synced": isinstance(lyrics, TimeSyncedLyrics),
                    "displayArtist": meta.primary_artist(),
                    "displayTitle": meta.title if meta.title else meta.display_title(),
                    "line": lines,
                }
            ]
        }
    }
    return response(request, data)


@subsonic_route("/search3")
async def search3(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/search3/
    query = request.query.get("query", "")
    artist_count = int(request.query.get("artistCount", 20))
    artist_offset = int(request.query.get("artistOffset", 0))
    album_count = int(request.query.get("albumCount", 20))
    album_offset = int(request.query.get("albumOffset", 0))
    song_count = int(request.query.get("songCount", 20))
    song_offset = int(request.query.get("songOffset", 0))

    if query == "":
        data = {
            "artist": SubsonicArrayArtistID3(conn, artist_count, artist_offset),
            "album": [
                SubsonicAlbumID3(conn, album, album_artist)
                for album, album_artist in conn.execute("SELECT DISTINCT album, album_artist FROM track")
            ],
            "song": SubsonicArrayChild(conn, song_count, song_offset),
        }
    else:
        data = {
            "artist": [],  # TODO
            "album": [
                SubsonicAlbumID3(conn, album.name, album.artist)
                for album in search.search_albums(conn, query, limit=album_count, offset=album_offset)
            ],
            "song": [
                SubsonicChild(conn, track, detailed=True)
                for track in search.search_tracks(conn, query, limit=song_count, offset=song_offset)
            ],
        }

    return response(request, {"searchResult3": data})


@subsonic_route("/getPlaylists")
async def getPlaylists(request: web.Request, conn: Connection, user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getplaylists/
    return response(request, {"playlists": SubsonicArrayPlaylist(conn, user)})


@subsonic_route("/getPlaylist")
async def getPlaylist(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getplaylist/
    playlist = from_id(request.query["id"])
    assert playlist
    return response(request, {"playlist": SubsonicPlaylist(conn, playlist, include_tracks=True)})


@subsonic_route("/scrobble")
async def scrobble(request: web.Request, conn: Connection, user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/scrobble/
    # TODO handle multiple id
    relpath = from_id(request.query["id"])
    timestamp = int(request.query.get("time", time.time()))
    submission = request.query.get("submission") == "true"

    player_id = user.username + request.query["c"]

    await activity.set_now_playing(conn, user, player_id, relpath, False, 0, 0, False, 1)

    if submission:
        track = Track.by_relpath(conn, relpath)
        if track:
            await activity.set_played(user, track, timestamp)

    return response(request, {})


@subsonic_route("/getRandomSongs")
async def getRandomSongs(request: web.Request, conn: Connection, _user: User):
    size = int(request.query.get("size", 10))

    # TODO 'genre' and 'musicFolderId' filters

    query = "SELECT path FROM track WHERE true"
    params: list[str | int] = []

    if "fromYear" in request.query:
        query += " AND year >= ?"
        params.append(int(request.query["fromYear"]))

    if "toYear" in request.query:
        query += " AND year <= ?"
        params.append(int(request.query["toYear"]))

    query += " ORDER BY RANDOM()"
    query += f" LIMIT {size}"

    data = {
        "randomSongs": {
            "song": [
                SubsonicChild(conn, Track.by_relpath(conn, relpath), detailed=True)
                for relpath, in conn.execute(query, params)
            ]
        }
    }

    return response(request, data)


@subsonic_route("/getGenres")
async def getGenres(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getgenres/
    return response(request, {"genres": {"genre": SubsonicArrayGenre(conn)}})


@subsonic_route("/getSongsByGenre")
async def getSongsByGenre(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getsongsbygenre/
    genre = request.query["genre"]
    count = int(request.query.get("count", 10))
    offset = int(request.query.get("offset", 0))

    data = {
        "songsByGenre": {
            "song": [
                SubsonicChild(conn, Track.by_relpath(conn, relpath), detailed=True)
                for relpath, in conn.execute(
                    f"""
                    SELECT track
                    FROM track_tag
                    WHERE tag = ?
                    LIMIT {count} OFFSET {offset}
                    """,
                    (genre,),
                ).fetchall()
            ]
        }
    }

    return response(request, data)


@subsonic_route("/getStarred")
async def getStarred(request: web.Request, _conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getstarred/
    data: dict[str, Any] = {
        "starred": {
            "artist": [],
            "album": [],
            "song": [],
        }
    }
    return response(request, data)


@subsonic_route("/getStarred2")
async def getStarred2(request: web.Request, _conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getstarred/
    data: dict[str, Any] = {
        "starred2": {
            "artist": [],
            "album": [],
            "song": [],
        }
    }
    return response(request, data)


@subsonic_route("/getArtistInfo2")
async def getArtistInfo2(request: web.Request, _conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getartistinfo2/
    data: dict[str, Any] = {"artistInfo2": {}}
    return response(request, data)


@subsonic_route("/getLicense")
async def getLicense(request: web.Request, _conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getlicense/
    data: dict[str, Any] = {"license": {"valid": True}}
    return response(request, data)


@subsonic_route("/getSimilarSongs2")
async def getSimilarSongs2(request: web.Request, conn: Connection, _user: User):
    # https://opensubsonic.netlify.app/docs/endpoints/getsimilarsongs2/
    artist = from_id(request.query["id"])
    count = int(request.query.get("count", 50))

    # Tempo calls getSimilarSongs with a track id, but OpenSubsonic documents `id` to be the artist id
    # https://github.com/CappielloAntonio/tempo/issues/326
    track = Track.by_relpath(conn, artist)
    if track:
        rows = conn.execute(
            f"""
            SELECT path
            FROM track JOIN track_tag ON path = track_tag.track
            WHERE tag IN (
                SELECT tag
                FROM track_tag
                WHERE track = ?
            )
            ORDER BY RANDOM()
            LIMIT {count}
            """,
            (track.relpath,),
        ).fetchall()
    else:
        rows = conn.execute(
            f"""
            SELECT path
            FROM track JOIN track_tag ON path = track_tag.track
            WHERE tag IN (
                SELECT tag
                FROM track_tag JOIN track_artist ON track_tag.track = track_artist.track
                WHERE artist = ?
            )
            ORDER BY RANDOM()
            LIMIT {count}
            """,
            (artist,),
        ).fetchall()

    data = {"similarSongs2": {"song": [SubsonicChild(conn, Track.by_relpath(conn, relpath)) for relpath, in rows]}}
    return response(request, data)


@subsonic_route("/updatePlaylist")
async def updatePlaylist(request: web.Request, conn: Connection, user: User):
    playlist_name = from_id(request.query["playlistId"])

    playlist = music.user_playlist(conn, playlist_name, user.user_id)
    if not user.admin and not playlist.write:
        raise web.HTTPForbidden(reason="no write access")

    for add in request.query.getall("songIdToAdd"):
        track = Track.by_relpath(conn, from_id(add))

        if track.playlist == playlist.name:
            continue

        await asyncio.to_thread(shutil.copy, track.path, playlist.path)

    await util.create_task(scanner.scan_playlist(user, playlist))

    raise web.HTTPNoContent()
