class Player {
    /** @type {HTMLAudioElement} */
    #htmlAudioElement;

    constructor() {
        document.addEventListener("DOMContentLoaded", () => {
            this.#htmlAudioElement = document.getElementById("audio");

            this.#htmlAudioElement.addEventListener('ended', () => queue.next());

            // Audio element should always be playing at max volume
            // Volume is set using GainNode in audio.js
            this.#htmlAudioElement.volume = 1;
        });

        eventBus.subscribe(MusicEvent.TRACK_CHANGE, track => {
            this.#replaceAudioSource(track);
            this.#replaceAlbumImages(track);
            this.#replaceTrackDisplayTitle(track);
        });

        eventBus.subscribe(MusicEvent.METADATA_CHANGE, updatedTrack => {
            if (queue.currentTrack
                && queue.currentTrack.track
                && queue.currentTrack.track.path
                && queue.currentTrack.track.path == updatedTrack.path) {
                console.debug('player: updating currently playing track following METADATA_CHANGE event');
                queue.currentTrack.track = updatedTrack;
                this.#replaceTrackDisplayTitle(queue.currentTrack);
            }
        });
    }

    /**
     * @returns {HTMLAudioElement}
     */
    getAudioElement() {
        return this.#htmlAudioElement ? this.#htmlAudioElement : document.getElementById("audio");
    }

    /**
     * @param {number} delta number of seconds to seek forwards, negative for backwards
     * @returns {void}
     */
    seekRelative(delta) {
        const newTime = this.#htmlAudioElement.currentTime + delta;
        if (newTime < 0) {
            this.#htmlAudioElement.currentTime = 0;
        } else if (newTime > this.#htmlAudioElement.duration) {
            this.#htmlAudioElement.currentTime = this.#htmlAudioElement.duration;
        } else {
            this.#htmlAudioElement.currentTime = newTime;
        }
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {Promise<void>}
     */
    async #replaceAudioSource(track) {
        this.#htmlAudioElement.src = track.audioUrl;
        try {
            await this.#htmlAudioElement.play();
        } catch (exception) {
            console.warn('player: failed to start playback: ', exception);
        }
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {void}
     */
    #replaceAlbumImages(track) {
        const cssUrl = `url("${track.imageUrl}")`;

        const bgBottom = document.getElementById('bg-image-1');
        const bgTop = document.getElementById('bg-image-2');
        const fgBottom = document.getElementById('album-cover-1');
        const fgTop = document.getElementById('album-cover-2');

        // Set bottom to new image
        bgBottom.style.backgroundImage = cssUrl;
        fgBottom.style.backgroundImage = cssUrl;

        // Slowly fade out old top image
        bgTop.style.opacity = 0;
        fgTop.style.opacity = 0;

        setTimeout(() => {
            // To prepare for next replacement, move bottom image to top image
            bgTop.style.backgroundImage = cssUrl;
            fgTop.style.backgroundImage = cssUrl;
            // Make it visible
            bgTop.style.opacity = 1;
            fgTop.style.opacity = 1;
        }, 200);
    }

    /**
     * @param {DownloadedTrack} track
     * @returns {void}
     */
    #replaceTrackDisplayTitle(track) {
        document.getElementById('current-track').replaceChildren(displayHtml(track.track, true));
        if (track.track !== null) {
            document.title = track.track.displayText(true, true);
        } else {
            document.title = '[track info unavailable]';
        }
    }
}

const player = new Player();
