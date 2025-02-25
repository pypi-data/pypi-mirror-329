class BrowseHistoryEntry {
    /** @type {string} */
    title;
    /** @type {object} */
    filters;
    constructor(title, filters) {
        this.title = title;
        this.filters = filters;
    }
}

class Browse {
    /** @type {Array<BrowseHistoryEntry>} */
    #history;
    constructor() {
        this.#history = [];

        eventBus.subscribe(MusicEvent.METADATA_CHANGE, () => {
            if (!windows.isOpen('window-browse')) {
                console.debug('browse: ignore METADATA_CHANGE, browse window is not open. Is editor open: ', windows.isOpen('window-editor'));
                return;
            }

            console.debug('browse: received METADATA_CHANGE, updating content');
            this.updateContent();
        });
    };

    /**
     * @returns {BrowseHistoryEntry}
     */
    current() {
        if (this.#history.length === 0) {
            throw new Exception();
        }

        return this.#history[this.#history.length - 1];
    }

    /**
     * @param {string} textContent
     */
    setHeader(textContent) {
        document.getElementById('window-browse').getElementsByTagName('h2')[0].textContent = textContent;
    };

    /**
     * @param {string} title
     * @param {Array<Filter>} filters
     */
    browse(title, filters) {
        windows.open('window-browse');
        if (!filters.playlist) {
            document.getElementById('browse-playlist').value = 'all';
        }
        this.#history.push(new BrowseHistoryEntry(title, filters));
        this.updateContent();
    };

    back() {
        if (this.#history.length < 2) {
            return;
        }
        this.#history.pop();
        this.updateContent();
    };

    async updateContent() {
        const table = document.getElementById('browse-table');
        const noContent = document.getElementById('browse-no-content');
        const loading = document.getElementById('browse-loading');
        const playlist = document.getElementById('browse-playlist');

        // Remove previous content, while new content is loading
        table.replaceChildren();
        loading.hidden = false;
        noContent.hidden = true;

        const current = this.current();
        this.setHeader(current.title);

        // update playlist dropdown from current filter
        if (current.filters.playlist) {
            playlist.value = current.filters.playlist;
        } else {
            playlist.value = 'all';
        }

        console.info('browse:', current);

        if (Object.keys(current.filters).length == 0) {
            noContent.hidden = false;
            loading.hidden = true;
            return;
        }

        const appendTracks = async tracks => {
            loading.hidden = true;
            await this.appendTrackRows(table, tracks);
        }

        await music.filterPages(current.filters, appendTracks);
    }

    /**
     * @param {string} artistName
     */
    browseArtist(artistName) {
        this.browse(T.browseArtist + artistName, {'artist': artistName});
    };

    /**
     * @param {string} albumName
     * @param {string} albumArtistName
     */
    browseAlbum(albumName, albumArtistName) {
        const title = T.browseAlbum + (albumArtistName === null ? '' : albumArtistName + ' - ') + albumName;
        const filters = {'album': albumName}
        if (albumArtistName) {
            filters.album_artist = albumArtistName;
        }
        this.browse(title, filters);
    };

    /**
     * @param {string} tagName
     */
    browseTag(tagName) {
        this.browse(T.browseTag + tagName, {'tag': tagName})
    };

    /**
     * @param {string} playlistName
     */
    browsePlaylist(playlistName) {
        this.browse(T.browsePlaylist + playlistName, {playlist: playlistName})
    };

    /**
     * @param {number} year
     */
    browseYear(year) {
        this.browse(T.browseYear + year, {year: year})
    }

    browseRecentlyAdded() {
        this.browse(T.browseRecentlyAdded, {order: "ctime", limit: 100});
    }

    browseRecentlyReleased() {
        this.browse(T.browseRecentlyReleased, {order: "year", limit: 100});
    }

    browseRandom() {
        this.browse(T.browseRandom, {order: "random", limit: 100});
    }

    browseMissingMetadata() {
        this.browse(T.browseMissingMetadata, {has_metadata: "0", order: "random", limit: 100});
    }

    browseNothing() {
        this.browse(T.browseNothing, {});
    };

    /**
     * also used by search.js
     * @param {HTMLTableElement} table
     * @param {Array<Track>} tracks
     */
    async appendTrackRows(table, tracks) {
        const addButton = createIconButton('playlist-plus');
        const editButton = createIconButton('pencil');
        const rows = [];
        for (const track of tracks) {
            const colPlaylist = document.createElement('td');
            colPlaylist.textContent = track.playlistName;

            const colDuration = document.createElement('td');
            colDuration.textContent = durationToString(track.duration);

            const colTitle = document.createElement('td');
            colTitle.appendChild(displayHtml(track));

            const addButton2 = addButton.cloneNode(true);
            addButton2.addEventListener('click', async () => {
                replaceIconButton(addButton2, 'loading');
                addButton2.firstChild.classList.add('spinning');
                addButton2.disabled = true;

                try {
                    const downloadedTrack = await track.download(...settings.getTrackDownloadParams());
                    queue.add(downloadedTrack, true);
                } catch (ex) {
                    console.error('browse: error adding track to queue', ex)
                }

                replaceIconButton(addButton2, 'playlist-plus')
                addButton2.firstChild.classList.remove('spinning');
                addButton2.disabled = false;
            });
            const colAdd = document.createElement('td');
            colAdd.appendChild(addButton2);
            colAdd.style.width = '2rem';

            const colEdit = document.createElement('td');
            colEdit.style.width = '2rem';

            if ((await music.playlist(track.playlistName)).write) {
                const editButton2 = editButton.cloneNode(true);
                editButton2.addEventListener('click', () => editor.open(track));
                colEdit.appendChild(editButton2);
            }

            const row = document.createElement('tr');
            row.append(colPlaylist, colDuration, colTitle, colAdd, colEdit);
            rows.push(row);
        }
        table.append(...rows);
    }
};

const browse = new Browse();

document.addEventListener('DOMContentLoaded', () => {
    // Playlist dropdown
    document.getElementById('browse-playlist').addEventListener('input', event => {
        console.debug('browse: filter-playlist input trigger');
        const playlist = event.target.value;
        const current = browse.current();
        // browse again, but with a changed playlist filter
        const newFilter = {...current.filters}
        if (playlist == 'all') {
            delete newFilter.playlist;
        } else {
            newFilter.playlist = playlist;
        }
        browse.browse(current.title, newFilter);
    });

    // Button to open browse window
    document.getElementById('browse-all').addEventListener('click', () => browse.browseNothing());

    // Back button in top left corner of browse window
    document.getElementById('browse-back').addEventListener('click', () => browse.back());

    // Button to jump to bottom
    const scroll = document.getElementById("browse-scroll");
    document.getElementById("browse-bottom").addEventListener("click", () => {
        scroll.scrollTo(0, scroll.scrollHeight, {'behavior': 'smooth'});
    });

    // Browse discover buttons
    document.getElementById("browse-recently-added").addEventListener("click", () => browse.browseRecentlyAdded());
    document.getElementById("browse-recently-released").addEventListener("click", () => browse.browseRecentlyReleased());
    document.getElementById("browse-random").addEventListener("click", () => browse.browseRandom());
    document.getElementById("browse-missing-metadata").addEventListener("click", () => browse.browseMissingMetadata());
});
