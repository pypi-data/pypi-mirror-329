const COLOR_MISSING_METADATA = "#ffc891"
const TRACK_INFO_UNAVAILABLE = document.createElement("span");
TRACK_INFO_UNAVAILABLE.style.color = COLOR_MISSING_METADATA;
TRACK_INFO_UNAVAILABLE.textContent = T.trackInfoUnavailable;

/**
 * Get display HTML for a track
 * @param {Track|null} track
 * @param {boolean} showPlaylist
 * @returns {HTMLSpanElement}
 */
function displayHtml(track, showPlaylist = false) {
    if (track == null) {
        return TRACK_INFO_UNAVAILABLE;
    }

    const html = document.createElement('span');
    html.classList.add('track-display-html');

    if (track.artists.length > 0 && track.title) {
        let first = true;
        for (const artist of track.artists) {
            if (first) {
                first = false;
            } else {
                html.append(', ');
            }

            const artistHtml = document.createElement('a');
            artistHtml.textContent = artist;
            artistHtml.addEventListener("click", () => browse.browseArtist(artist));
            html.append(artistHtml);
        }

        html.append(' - ' + track.title);
    } else {
        const span = document.createElement('span');
        span.style.color = COLOR_MISSING_METADATA;
        span.textContent = track.path.substring(track.path.indexOf('/') + 1);
        html.append(span);
    }

    const secondary = document.createElement('span');
    secondary.classList.add('secondary');
    secondary.append(document.createElement('br'));
    html.append(secondary);

    if (showPlaylist) {
        const playlistHtml = document.createElement('a');
        playlistHtml.addEventListener("click", () => browse.browsePlaylist(track.playlistName));
        playlistHtml.textContent = track.playlistName;
        secondary.append(playlistHtml);
    }

    if (track.year || track.album) {
        if (showPlaylist) {
            secondary.append(', ');
        }

        if (track.album) {
            const albumLink = document.createElement('a');
            albumLink.addEventListener("click", () => browse.browseAlbum(track.album, track.albumArtist));
            if (track.albumArtist) {
                albumLink.textContent = track.albumArtist + ' - ' + track.album;
            } else {
                albumLink.textContent = track.album;
            }
            secondary.append(albumLink);
            if (track.year) {
                secondary.append(', ');
            }
        }

        if (track.year) {
            const yearLink = document.createElement('a');
            yearLink.textContent = track.year;
            yearLink.addEventListener('click', () => browse.browseYear(track.year));
            secondary.append(yearLink);
        }
    }

    return html;
};
