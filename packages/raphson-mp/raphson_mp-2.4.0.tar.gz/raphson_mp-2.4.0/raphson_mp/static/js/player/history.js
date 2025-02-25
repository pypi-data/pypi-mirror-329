const PLAYED_TIMER_INTERVAL_SECONDS = 5;

class History {
    /** @type {boolean} */
    hasScrobbled;
    /** @type {number} */
    playCounter;
    /** @type {number} */
    requiredPlayingCounter;
    /** @type {number} */
    startTimestamp;

    constructor() {
        eventBus.subscribe(MusicEvent.TRACK_CHANGE, () => this.#onNewTrack());
        setInterval(() => this.#update(), PLAYED_TIMER_INTERVAL_SECONDS * 1000);
    }

    #onNewTrack() {
        this.hasScrobbled = false;
        this.playingCounter = 0;
        this.startTimestamp = Math.floor((new Date()).getTime() / 1000);
        // last.fm requires track to be played for half its duration or for 4 minutes (whichever is less)
        if (queue.currentTrack && queue.currentTrack.track) {
            this.requiredPlayingCounter = Math.min(4*60, Math.round(queue.currentTrack.track.duration / 2));
        } else {
            this.requiredPlayingCounter = null;
        }
    }

    async #update() {
        if (this.hasScrobbled) {
            return;
        }

        if (this.requiredPlayingCounter == null) {
            console.debug('history: no current track');
            return;
        }

        const audioElem = player.getAudioElement();

        if (audioElem.paused) {
            console.debug('history: audio element paused');
            return;
        }

        this.playingCounter += PLAYED_TIMER_INTERVAL_SECONDS;

        console.debug('history: playing, counter:', this.playingCounter, '/', this.requiredPlayingCounter);

        if (this.playingCounter > this.requiredPlayingCounter) {
            console.info('history: played');
            this.hasScrobbled = true;
            await music.played(queue.currentTrack.track, this.startTimestamp);
        }
    }
}

const history = new History();
