class PlayerLyrics {
    /** @type {HTMLAudioElement} */
    #htmlAudio;
    /** @type {HTMLInputElement} */
    #htmlLyricsSetting;
    /** @type {HTMLDivElement} */
    #htmlLyricsBox;
    #lastLine = null;
    #updateSyncedLyricsListener;

    constructor() {
        this.#updateSyncedLyricsListener = () => this.#updateSyncedLyrics();

        document.addEventListener("DOMContentLoaded", () => {
            this.#htmlAudio = document.getElementById("audio");
            this.#htmlLyricsSetting = document.getElementById("settings-lyrics");
            this.#htmlLyricsBox = document.getElementById('lyrics-box');

            // Quick toggle for lyrics setting
            document.getElementById('album-cover-box').addEventListener('click', () => this.toggleLyrics());

            // Listener is only registered if page is visible, so if page visibility
            // changes we must register (or unregister) the listener.
            document.addEventListener('visibilitychange', () => this.#registerListener());

            // Handle lyrics setting being changed
            this.#htmlLyricsSetting.addEventListener('change', () => {
                this.#replaceLyrics();
                coverSize.resizeCover();
            });
        });

        eventBus.subscribe(MusicEvent.TRACK_CHANGE, () => {
            // When track changes, current state is no longer accurate
            this.#lastLine = null;
            this.#replaceLyrics();
        });
    }

    toggleLyrics() {
        this.#htmlLyricsSetting.checked = !this.#htmlLyricsSetting.checked;
        this.#htmlLyricsSetting.dispatchEvent(new Event('change'));
    }

    #updateSyncedLyrics() {
        const lyrics = queue.currentTrack.lyrics;
        const currentLine = lyrics.currentLine(this.#htmlAudio.currentTime);

        if (currentLine == this.#lastLine) {
            // Still the same line, no need to cause expensive DOM update.
            return;
        }

        this.#lastLine = currentLine;

        // Show current line, with context
        const context = 3;
        const lyricsHtml = [];
        for (let i = currentLine - context; i <= currentLine + context; i++) {
            if (i >= 0 && i < lyrics.text.length) {
                const lineHtml = document.createElement('span');
                lineHtml.textContent = lyrics.text[i].text;
                if (i != currentLine) {
                    lineHtml.classList.add('secondary-large');
                }
                lyricsHtml.push(lineHtml);
            }
            lyricsHtml.push(document.createElement('br'));
        }

        this.#htmlLyricsBox.replaceChildren(...lyricsHtml);
    }

    #registerListener() {
        if (document.visibilityState == 'visible'
            && queue.currentTrack
            && queue.currentTrack.lyrics
            && queue.currentTrack.lyrics instanceof TimeSyncedLyrics
            && this.#htmlLyricsSetting.checked
        ) {
            console.debug('lyrics: registered timeupdate listener');
            this.#htmlAudio.removeEventListener('timeupdate', this.#updateSyncedLyricsListener); // remove it in case it is already registered
            this.#htmlAudio.addEventListener('timeupdate', this.#updateSyncedLyricsListener);
            // also trigger immediate update, especially necessary when audio is paused and no timeupdate events will be triggered
            this.#updateSyncedLyrics();
        } else {
            console.debug('lyrics: unregistered timeupdate listener');
            this.#htmlAudio.removeEventListener('timeupdate', this.#updateSyncedLyricsListener);
        }
    }

    #replaceLyrics() {
        const queuedTrack = queue.currentTrack;

        const showLyrics = queuedTrack && queuedTrack.lyrics && this.#htmlLyricsSetting.checked;

        this.#htmlLyricsBox.hidden = !showLyrics;

        if (showLyrics && queuedTrack.lyrics instanceof PlainLyrics) {
            this.#htmlLyricsBox.textContent = queuedTrack.lyrics.text;
        }

        // time-synced lyrics is handled by updateSyncedLyrics
        this.#registerListener();
    }
}

const lyrics = new PlayerLyrics();
