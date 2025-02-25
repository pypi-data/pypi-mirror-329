"use strict";

// Common JavaScript interface to API, to be used by the music player and other pages.
// Scripts using this API must provide a CSRF_TOKEN global variable with the CSRF token (not very portable, should change at some point).

const ControlCommand = {
    CLIENT_PLAYING: "c_playing",
    CLIENT_SUBSCRIBE: "c_subscribe",
    CLIENT_TOKEN: "c_token",
    CLIENT_PLAY: "c_play",
    CLIENT_PAUSE: "c_pause",
    CLIENT_PREVIOUS: "c_previous",
    CLIENT_NEXT: "c_next",
    SERVER_PLAYING: "s_playing",
    SERVER_PLAYED: "s_played",
    SERVER_PLAYING_STOPPED: "s_playing_stopped",
    SERVER_FILE_CHANGE: "s_file_change",
    SERVER_PLAY: "s_play",
    SERVER_PAUSE: "s_pause",
    SERVER_PREVIOUS: "s_previous",
    SERVER_NEXT: "s_next",
};

const ControlTopic = {
    ACTIVITY: "activity",
};

class ControlChannel {
    /** @type {string} */
    #id;
    /** @type {Array<string>} */
    #subscriptions;
    /** @type {Object<string, Array<function>>} */
    #handlers;
    /** @type {Array<Function>} */
    #onConnect;
    /** @type {WebSocket} */
    #socket;
    constructor() {
        this.#id = uuidv4();
        this.#subscriptions = [];
        this.#handlers = {};
        this.#onConnect = [];
        this.#socket = null;

        for (const command of Object.values(ControlCommand)) {
            this.#handlers[command] = [];
        }

        if (!OFFLINE_MODE) {
            setInterval(() => {
                if (this.#socket.readyState != this.#socket.CONNECTING
                    && this.#socket.readyState != this.#socket.OPEN
                ) {
                    this.#open();
                }
            }, 10000);

            this.#open();
        }
    }

    #open() {
        // Modern browsers (since early 2024) have support for connecting to a partial URL (just "/control?id=...").
        // However, we need to support earlier versions, especially because of mobile Safari and Firefox ESR in Linux distributions.
        // So, construct a URL manually:
        var url = new URL('/control?id=' + encodeURIComponent(this.#id), window.location.href);
        url.protocol = url.protocol.replace('http', 'ws'); // http -> ws, https -> wss
        console.info('ws: connect:', url.href);
        this.#socket = new WebSocket(url.href);

        this.#socket.addEventListener("message", event => this.#handleMessage(event.data));

        // Reissue previous subscriptions when socket is opened
        this.#socket.addEventListener("open", () => {
            this.sendMessage(ControlCommand.CLIENT_TOKEN, {"csrf": CSRF_TOKEN});
            for (const func of this.#onConnect) {
                func();
            }
            for (const topic of this.#subscriptions) {
                this.sendMessage(ControlCommand.CLIENT_SUBSCRIBE, {"topic": topic});
            }
        });
    }

    /**
     * @param {string} message
     */
    #handleMessage(message) {
        message = JSON.parse(message);
        console.debug('api: ws: received:', message);
        if (message.name in this.#handlers) {
            for (const handler of this.#handlers[message.name]) {
                handler(message);
            }
        } else {
            console.warn("ws: received command is unknown")
        }
    }

    /**
     * @param {string} name
     * @param {Object} data
     */
    sendMessage(name, data) {
        if (this.#socket == null || this.#socket.readyState != WebSocket.OPEN) {
            console.warn('api: ws: disconnected, cannot send:', name)
            return;
        }
        console.debug('api: ws: send:', name, data)
        this.#socket.send(JSON.stringify({"name": name, ...data}))
    }

    /**
     * @param {string} command
     * @param {function} handler
     */
    registerMessageHandler(command, handler) {
        this.#handlers[command].push(handler)
    }

    registerConnectHandler(handler) {
        this.#onConnect.push(handler);
    }

    /**
     * @param {string} command
     */
    subscribe(topic) {
        this.#subscriptions.push(topic);
        this.sendMessage(ControlCommand.CLIENT_SUBSCRIBE, {"topic": topic});
    }

    async play(player_id) {
        this.sendMessage(ControlCommand.CLIENT_PLAY, {player_id: player_id});
    }

    async pause(player_id) {
        this.sendMessage(ControlCommand.CLIENT_PAUSE, {player_id: player_id});
    }

    async previous(player_id) {
        this.sendMessage(ControlCommand.CLIENT_PREVIOUS, {player_id: player_id});
    }

    async next(player_id) {
        this.sendMessage(ControlCommand.CLIENT_NEXT, {player_id: player_id});
    }

    sendStopSignal() {
        const data = new FormData();
        data.set("csrf", CSRF_TOKEN)
        data.set("id", this.#id);
        navigator.sendBeacon("/activity/stop", data);
    }
}

const controlChannel = new ControlChannel();

class Album {
    /** @type {string} */
    name;
    /** @type {string|null} */
    artist;
    /** @type {string} */
    track; // arbitrary track from album to get cover image
    constructor(albumObj) {
        this.name = albumObj.name;
        this.artist = albumObj.artist;
        this.track = albumObj.track;
    }

    /**
     * @param {string} imageQuality 'low' or 'high'
     * @param {boolean} stream
     * @param {boolean} memeCover
     * @returns {Promise<URL>}
     */
    async getCover(imageQuality, stream, memeCover) {
        const imageUrl = `/track/${encodeURIComponent(this.track)}/cover?quality=${imageQuality}&meme=${memeCover ? 1 : 0}`;
        if (stream) {
            return imageUrl;
        } else {
            const coverResponse = await fetch(imageUrl);
            checkResponseCode(coverResponse);
            const imageBlob = await coverResponse.blob();
            console.debug('api: downloaded image', imageUrl);
            return URL.createObjectURL(imageBlob);
        }
    }
}

class SearchResult {
    /** @type {Array<Track>} */
    tracks;
    /** @type {Album} */
    albums;
    constructor(tracks, albums) {
        this.tracks = tracks;
        this.albums = albums;
    }
}

class Music {
    /** @type {Array<Playlist>} */
    #playlists;

    constructor() {}

    /**
     * @returns {Promise<Array<Playlist>>}
     */
    async playlists() {
        // has to be an anonymous function assigned to a variable instead of a normal function or 'this' is not available
        const retrievePlaylists = async () => {
            if (this.#playlists == undefined) {
                const response = await fetch('/playlist/list');
                checkResponseCode(response);
                const json = await response.json();
                this.#playlists = [];
                for (const playlistObj of json) {
                    this.#playlists.push(new Playlist(playlistObj));
                }
            }
        }

        if (navigator.locks) {
            await navigator.locks.request("api_playlists", retrievePlaylists);
        } else {
            console.warn('navigator.locks not available, redundant requests may happen');
            await retrievePlaylists();
        }

        return this.#playlists;
    }

    /**
     * @param {string} name
     * @returns {Promise<Playlist>}
     */
    async playlist(name) {
        const playlists = await this.playlists();
        for (const playlist of playlists) {
            if (playlist.name == name) {
                return playlist;
            }
        }
        return null;
    }

    /**
     * @param {Array<object>} json
     * @returns {Array<Track>}
     */
    #tracksFromJson(json) {
        const tracks = [];
        for (const trackObj of json) {
            tracks.push(new Track(trackObj));
        }
        return tracks;
    }

    /**
     * @param {Array<object>} json
     * @returns {Array<Album>}
     */
    #albumsFromJson(json) {
        const albums = [];
        for (const album of json) {
            albums.push(new Album(album));
        }
        return albums
    }

    /**
     * @param {object} filters with key = playlist, artist, album_artist, album, etc.
     * @returns {Promise<Array<Track>>}
     */
    async filter(filters) {
        const encodedFilters = [];
        for (const filter in filters) {
            encodedFilters.push(filter + '=' + encodeURIComponent(filters[filter]));
        }
        const response = await fetch('/tracks/filter?' + encodedFilters.join('&'));
        checkResponseCode(response);
        const json = await response.json();
        return this.#tracksFromJson(json.tracks);
    }

    /**
     * Paginated alternative to filter()
     * @param {object} filters
     * @param {any} callback function that accepts a list of tracks TODO type
     */
    async filterPages(filters, callback) {
        const totalLimit = filters.limit ? filters.limit : 5000;
        filters.limit = Math.min(1000, totalLimit);
        filters.offset = 0;
        while (true) {
            console.debug('api: filter', filters);
            const tracks = await this.filter(filters);
            await callback(tracks);
            filters.offset += tracks.length;
            if (tracks.length < filters.limit || filters.offset >= totalLimit) {
                break;
            }
        }
    }

    /**
     * @param {string} query FTS5 search query
     * @returns {Promise<SearchResult>}
     */
    async search(query) {
        const response = await fetch('/tracks/search?query=' + encodeURIComponent(query));
        checkResponseCode(response);
        const json = await response.json();
        const tracks = this.#tracksFromJson(json.tracks);
        const albums = this.#albumsFromJson(json.albums);
        return new SearchResult(tracks, albums);
    }

    /**
     * @param {string} path
     * @returns {Promise<Track>}
     */
    async track(path) {
        const response = await fetch(`/track/info${encodeURIComponent(path)}/info`);
        checkResponseCode(response);
        return new Track(await response.json());
    }

    /**
     * @returns {Promise<Array<string>>}
     */
    async tags() {
        const response = await fetch('/tracks/tags');
        checkResponseCode(response);
        return await response.json();
    }

    /**
     * @param {track} track
     */
    async played(track, startTimestamp) {
        const data = {
            track: track.path,
            timestamp: startTimestamp,
        }
        await jsonPost('/activity/played', data);
    }

    /**
     * @param {string} url
     * @returns {Promise<DownloadedTrack>}
     */
    async downloadTrackFromWeb(url) {
        const audioResponse = await fetch('/download/ephemeral?url=' + encodeURIComponent(url));
        checkResponseCode(audioResponse);
        const audio = URL.createObjectURL(await audioResponse.blob());
        const image = '/static/img/raphson_small.webp';
        return new DownloadedTrack(null, audio, image, null);
    }

    /**
     * @returns {Promise<DownloadedTrack|null>}
     */
    async downloadNews() {
        const audioResponse = await fetch('/news/audio');
        if (audioResponse.status == 503) {
            return null;
        }
        checkResponseCode(audioResponse);
        const audioBlob = URL.createObjectURL(await audioResponse.blob());

        const imageUrl = '/static/img/raphson.png';

        return new DownloadedTrack(null, audioBlob, imageUrl, null);
    }

    /**
     * @param {Playlist} playlist Playlist
     * @param {number} index Hotkey number, set to >=10 to not assign a hotkey
     * @param {boolean} defaultChecked Whether checkbox should be checked
     * @returns {HTMLSpanElement}
     */
    #createPlaylistCheckbox(playlist, index, defaultChecked) {
        const input = document.createElement("input");
        input.type = 'checkbox';
        input.dataset.playlist = playlist.name;
        input.id = uuidv4();
        input.checked = defaultChecked;

        const sup = document.createElement('sup');
        if (index < 10) { // Assume number keys higher than 9 don't exist
            sup.textContent = index;
        }

        const trackCount = document.createElement('span');
        trackCount.classList.add('secondary');
        trackCount.textContent = ' ' + playlist.trackCount;

        const label = document.createElement("label");
        label.htmlFor = input.id;
        label.textContent = playlist.name;
        label.replaceChildren(playlist.name, sup, trackCount);

        // Checkbox and label must always be together
        const span = document.createElement("div");
        span.replaceChildren(input, label);

        return span;
    }

    /**
     * @returns {Promise<HTMLDivElement>}
     */
    async getPlaylistCheckboxes(ignoreEmpty = true) {
        const mainDiv = document.createElement('div');
        const otherDiv = document.createElement('div');
        mainDiv.classList.add('playlist-checkboxes');
        otherDiv.classList.add('playlist-checkboxes');

        let index = 1;
        for (const playlist of await this.playlists()) {
            if (ignoreEmpty && playlist.trackCount == 0) {
                continue;
            }

            if (playlist.favorite) {
                mainDiv.appendChild(this.#createPlaylistCheckbox(playlist, index++, true));
            } else {
                otherDiv.appendChild(this.#createPlaylistCheckbox(playlist, 10, false));
            }
        }

        const parent = document.createElement('div');
        parent.replaceChildren(mainDiv, otherDiv);
        return parent;
    }
}

const music = new Music();

class Playlist {
    /** @type {string} */
    name;
    /** @type {number} */
    trackCount;
    /** @type {boolean} */
    favorite;
    /** @type {boolean} */
    write;

    /**
     * @param {Object.<string, string|boolean|number} objectFromApi
     */
    constructor(objectFromApi) {
        this.name = objectFromApi.name;
        this.trackCount = objectFromApi.track_count;
        this.favorite = objectFromApi.favorite;
        this.write = objectFromApi.write;
    }

    async chooseRandomTrack(requireMetadata, tagFilter) {
        const chooseResponse = await jsonPost('/playlist/' + encodeURIComponent(this.name) + '/choose_track', {'require_metadata': requireMetadata, ...tagFilter});
        const trackData = await chooseResponse.json();
        console.info('api: chosen track', trackData.path);
        return new Track(trackData);
    }
}

/**
 * Metadata suggested by AcoustID
 */
class SuggestedMetadata {
    /** @type {string} */
    id;
    /** @type {string} */
    title;
    /** @type {Array<string>} */
    artists;
    /** @type {string} */
    album;
    /** @type {string} */
    albumArtist;
    /** @type {number | null} */
    year;
    /** @type {string} */
    releaseType;
    /** @type {string} */
    packaging;

    constructor(metaObj) {
        this.id = metaObj.id;
        this.title = metaObj.title;
        this.artists = metaObj.artists;
        this.album = metaObj.album;
        this.albumArtist = metaObj.album_artist;
        this.year = metaObj.year;
        this.releaseType = metaObj.release_type;
        this.packaging = metaObj.packaging;
    }
}

class Track {
    /** @type {string} */
    path;
    /** @type {string} */
    playlistName;
    /** @type {number} */
    duration;
    /** @type {Array<string>} */
    tags;
    /** @type {string | null} */
    title;
    /** @type {Array<string>} */
    artists;
    /** @type {string | null} */
    album;
    /** @type {string | null} */
    albumArtist;
    /** @type {number | null} */
    year;
    /** @type {string | null} */
    video;
    /** @type {string | null} */
    lyrics;

    constructor(trackData) {
        this.#updateLocalVariablesFromTrackDataResponse(trackData);
    };

    #updateLocalVariablesFromTrackDataResponse(trackData) {
        this.path = trackData.path;
        this.playlistName = trackData.playlist;
        this.duration = trackData.duration;
        this.tags = trackData.tags;
        this.title = trackData.title;
        this.artists = trackData.artists;
        this.album = trackData.album;
        this.albumArtist = trackData.album_artist;
        this.year = trackData.year;
        this.video = trackData.video;
        this.lyrics = trackData.lyrics;
    }

    /**
     * Generates display text for this track
     * @param {boolean} showPlaylist
     * @returns {string}
     */
    displayText(showPlaylist = false, showAlbum = false) {
        let text = '';

        if (showPlaylist) {
            text += `${this.playlistName}: `
        }

        if (this.artists !== null && this.title !== null) {
            text += this.artists.join(', ');
            text += ' - ';
            text += this.title;
        } else {
            text += this.path.substring(this.path.indexOf('/') + 1);
        }

        if (this.album && showAlbum) {
            text += ` (${this.album}`;
            if (this.year) {
                text += `, ${this.year})`;
            } else {
                text += ')';
            }
        } else if (this.year) {
            text += ` (${this.year})`;
        }

        return text;
    };

    /**
     * @param {string} audioType
     * @param {boolean} stream
     * @returns {Promise<string>} URL
     */
    async getAudio(audioType, stream) {
        const audioUrl = `/track/${encodeURIComponent(this.path)}/audio?type=${audioType}`;
        if (stream) {
            return audioUrl;
        } else {
            const trackResponse = await fetch(audioUrl);
            checkResponseCode(trackResponse);
            const audioBlob = await trackResponse.blob();
            console.debug('api: downloaded audio', audioUrl);
            return URL.createObjectURL(audioBlob);
        }
    }

    getAlbum() {
        return new Album({'name': this.album, 'artist': this.albumArtist, 'track': this.path});
    }

    /**
     * @returns {Promise<Lyrics|null>}
     */
    async getLyrics() {
        const lyricsUrl = `/track/${encodeURIComponent(this.path)}/lyrics`;
        const lyricsResponse = await fetch(lyricsUrl);
        checkResponseCode(lyricsResponse);
        const lyricsJson = await lyricsResponse.json();
        console.debug('api: downloaded lyrics', lyricsUrl);
        switch(lyricsJson.type) {
            case "none":
                return null;
            case "synced":
                const lines = [];
                for (const line of lyricsJson.text) {
                    lines.push(new LyricsLine(line.start_time, line.text));
                }
                return new TimeSyncedLyrics(lyricsJson.source, lines);
            case "plain":
                return new PlainLyrics(lyricsJson.source, lyricsJson.text);
        }
    }

    /**
     * @param {string} audioType
     * @param {boolean} stream
     * @param {boolean} memeCover
     * @returns {Promise<DownloadedTrack>}
     */
    async download(audioType='webm_opus_high', stream=false, memeCover=false) {
        // Download audio, cover, lyrics in parallel
        const promises = [
            this.getAudio(audioType, stream),
            this.getAlbum().getCover(audioType == 'webm_opus_low' ? 'low' : 'high', stream, memeCover),
            this.getLyrics(),
        ];
        return new DownloadedTrack(this, ...(await Promise.all(promises)));
    }

    async delete() {
        const oldName = this.path.split('/').pop();
        const newName = '.trash.' + oldName;
        await jsonPost('/files/rename', {path: this.path, new_name: newName});
    }

    async dislike() {
        await jsonPost('/dislikes/add', {track: this.path});
    }

    /**
     * Updates track metadata by sending current metadata of this object to the server.
     */
    async saveMetadata() {
        const payload = {
            title: this.title,
            album: this.album,
            artists: this.artists,
            album_artist: this.albumArtist,
            tags: this.tags,
            year: this.year,
            lyrics: this.lyrics,
        };

        await jsonPost(`/track/${encodeURIComponent(this.path)}/update_metadata`, payload);
    }

    /**
     * Copy track to other playlist
     * @param {string} playlistName
     * @returns {Promise<void>}
     */
    async copyTo(playlistName) {
        await jsonPost('/player/copy_track', {track: this.path, playlist: playlistName});
    }

    async refresh() {
        const json = await jsonGet(`/track/${encodeURIComponent(this.path)}/info`);
        this.#updateLocalVariablesFromTrackDataResponse(json);
    }

    /**
     * Look up metadata for this track using the AcoustID service
     * @returns {Promise<Array<SuggestedMetadata>>}
     */
    async acoustid() {
        const json = await jsonGet(`/track/${encodeURIComponent(this.path)}/acoustid`)
        const array = [];
        for (const meta of json) {
            array.push(new SuggestedMetadata(meta));
        }
        return array;
    }

    getVideoURL() {
        return `/track/${encodeURIComponent(this.path)}/video`
    }
}

class DownloadedTrack {
    /**
     * @type {Track|null} Null for virtual tracks, like news
     */
    track;
    /**
     * @type {string}
     */
    audioUrl;
    /**
     * @type {string}
     */
    imageUrl;
    /**
     * @type {Lyrics|null}
     */
    lyrics;

    /**
     *
     * @param {Track|null} track
     * @param {string} audioUrl
     * @param {string} imageUrl
     * @param {Lyrics|null} lyrics
     */
    constructor(track, audioUrl, imageUrl, lyrics) {
        this.track = track;
        this.audioUrl = audioUrl;
        this.imageUrl = imageUrl;
        this.lyrics = lyrics;
    }

    revokeObjects() {
        // audioUrl and imageUrl are not always object URLs. If they are not, revokeObjectURL does not raise an error.
        URL.revokeObjectURL(this.audioUrl);
        URL.revokeObjectURL(this.imageUrl);
    }
}

class Lyrics {
    /** @type {string | null} */
    source;
    constructor(source) {
        this.source = source;
    };
};

class PlainLyrics extends Lyrics {
    /** @type {string} */
    text;
    constructor(source, text) {
        super(source)
        this.text = text;
    };
};

class LyricsLine {
    /** @type {number} */
    startTime;
    /** @type {string} */
    text;
    constructor(startTime, text) {
        this.startTime = startTime;
        this.text = text;
    }
}

class TimeSyncedLyrics extends Lyrics {
    /** @type {Array<LyricsLine>} */
    text;
    constructor(source, text) {
        super(source);
        this.text = text;
    };

    /**
     * @returns {string}
     */
    asPlainText() {
        const lines = [];
        for (const line of this.text) {
            lines.push(line.text);
        }
        return lines.join('\n');
    }

    /**
     * @param {number} currentTime
     * @returns {number}
     */
    currentLine(currentTime) {
        currentTime += 0.5; // go to next line slightly earlier, to give the user time to read
        // current line is the last line where currentTime is after the line start time
        for (let i = 0; i < this.text.length; i++) {
            if (currentTime < this.text[i].startTime) {
                return i - 1;
            }
        }
        return this.text.length - 1;
    }
};
