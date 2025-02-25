from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from typing import Any

from aiohttp import ClientSession

from raphson_mp.client.share import Share
from raphson_mp.common.image import ImageFormat, ImageQuality
from raphson_mp.common.lyrics import LyricsLine, PlainLyrics, TimeSyncedLyrics
from raphson_mp.common.track import AudioFormat
from raphson_mp.util import urlencode


@dataclass
class DownloadedTrack:
    track: Track | None
    audio: bytes
    image: bytes
    lyrics_json: str

    @property
    def lyrics(self) -> TimeSyncedLyrics | PlainLyrics | None:
        lyrics_dict = json.loads(self.lyrics_json)
        if lyrics_dict["type"] == "none":
            return None
        elif lyrics_dict["type"] == "plain":
            return PlainLyrics(lyrics_dict["source"], lyrics_dict["text"])
        elif lyrics_dict["type"] == "synced":
            text = [LyricsLine(line["start_time"], line["text"]) for line in lyrics_dict["text"]]
            return TimeSyncedLyrics(lyrics_dict["source"], text)
        else:
            raise ValueError()

    @property
    def lyrics_text(self) -> str | None:
        lyrics = self.lyrics
        if not lyrics:
            return None
        if isinstance(lyrics, TimeSyncedLyrics):
            lyrics = lyrics.to_plain()
        return lyrics.text


@dataclass
class Track:
    path: str
    display: str
    mtime: int
    ctime: int
    duration: int
    title: str | None
    album: str | None
    album_artist: str | None
    year: int | None
    artists: list[str]
    tags: list[str]
    video: str | None
    _session: ClientSession | None = None

    @property
    def playlist(self):
        return self.path[self.path.index("/") :]

    @classmethod
    def from_dict(cls, json_data: Any, session: ClientSession | None = None):
        return cls(
            json_data["path"],
            json_data["display"],
            json_data["mtime"],
            json_data["ctime"] if "ctime" in json_data else json_data["mtime"],  # handle server versions before 2.3.0
            json_data["duration"],
            json_data["title"],
            json_data["album"],
            json_data["album_artist"],
            json_data["year"],
            json_data["artists"],
            json_data["tags"],
            json_data["video"],
            session,
        )

    def to_dict(self) -> dict[str, str | int | list[str] | None]:
        return {
            "path": self.path,
            "display": self.display,
            "mtime": self.mtime,
            "ctime": self.ctime,
            "duration": self.duration,
            "title": self.title,
            "album": self.album,
            "album_artist": self.album_artist,
            "year": self.year,
            "artists": self.artists,
            "tags": self.tags,
            "video": self.video,
        }

    async def get_audio(self, audio_format: AudioFormat) -> bytes:
        assert self._session, "track has no ClientSession"
        async with self._session.get(
            "/track/" + urlencode(self.path) + "/audio?type=" + audio_format.value
        ) as response:
            return await response.content.read()

    async def get_cover_image(
        self, quality: ImageQuality = ImageQuality.HIGH, format: ImageFormat = ImageFormat.WEBP, meme: bool = False
    ) -> bytes:
        assert self._session, "track has no ClientSession"
        async with self._session.get(
            "/track/" + urlencode(self.path) + "/cover",
            params={"quality": quality.value, "format": format.value, "meme": 1 if meme else 0},
        ) as response:
            return await response.content.read()

    async def get_lyrics_json(self) -> str:
        assert self._session, "track has no ClientSession"
        async with self._session.get("/track/" + urlencode(self.path) + "/lyrics") as response:
            return await response.text()

    async def download(self, audio_format: AudioFormat = AudioFormat.WEBM_OPUS_HIGH) -> DownloadedTrack:
        audio, image, lyrics_json = await asyncio.gather(
            self.get_audio(audio_format),
            self.get_cover_image(),
            self.get_lyrics_json(),
        )
        return DownloadedTrack(self, audio, image, lyrics_json)

    async def download_mp3(self):
        return await self.get_audio(AudioFormat.MP3_WITH_METADATA)

    async def share(self) -> Share:
        assert self._session, "track has no ClientSession"
        async with self._session.post("/share/create", json={"track": self.path}) as response:
            code = (await response.json())["code"]
            return Share(code, self._session)
