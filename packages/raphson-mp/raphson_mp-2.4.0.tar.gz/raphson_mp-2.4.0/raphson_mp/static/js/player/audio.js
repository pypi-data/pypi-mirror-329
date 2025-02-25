class Audio {
    /** @type {HTMLInputElement} */
    #htmlVolume;
    /** @type {HTMLInputElement} */
    #htmlGain;
    /** @type {number} */
    fftSize = 2**13;
    /** @type {AudioContext} */
    #audioContext;
    /** @type {GainNode} */
    #gainNode = null;
    /** @type {AnalyserNode} */
    analyser = null;

    constructor() {
        eventBus.subscribe(MusicEvent.SETTINGS_LOADED, () => {
            this.#updateSliderIcon();
        });

        document.addEventListener('DOMContentLoaded', () => {
            this.#htmlVolume = document.getElementById('settings-volume');
            this.#htmlGain = document.getElementById('settings-audio-gain');

            // Respond to gain changes
            this.#htmlGain.addEventListener('change', event => {
                this.#applyGain();
            });

            // Respond to volume button changes
            // Event fired when input value changes, also manually when code changes the value
            this.#htmlVolume.addEventListener('change', () => {
                this.#updateSliderIcon();
                this.#applyGain();
            });
            // Also respond to input event, so volume changes immediately while user is dragging slider
            this.#htmlVolume.addEventListener('input', () => {
                this.#updateSliderIcon();
                this.#applyGain();
            });

            // Unfocus after use so arrow hotkeys still work for switching tracks
            this.#htmlVolume.addEventListener('mouseup', () => this.#htmlVolume.blur())

            // Scroll to change volume
            this.#htmlVolume.addEventListener('wheel', event => {
                this.setVolume(this.getVolume() + (event.deltaY < 0 ? 0.05 : -0.05));
            }, {passive: true});

            // Can only create AudioContext once media is playing
            player.getAudioElement().addEventListener('play', () => {
                if (this.#audioContext) {
                    return;
                }
                console.debug('audiocontext: create');
                this.#audioContext = new AudioContext();
                const source = this.#audioContext.createMediaElementSource(player.getAudioElement());
                this.analyser = this.#audioContext.createAnalyser(); // used by visualiser
                this.analyser.fftSize = this.fftSize;
                this.#gainNode = this.#audioContext.createGain();
                this.#applyGain(); // If gain was set while audio was still paused
                source.connect(this.analyser);
                source.connect(this.#gainNode);
                this.#gainNode.connect(this.#audioContext.destination);
            });
        });
    }

    /**
     * @returns {number} volume 0.0-1.0
     */
    getVolume() {
        return parseInt(this.#htmlVolume.value) / 100.0;
    }

    /**
     * @param {number} volume 0.0-1.0, outside of this range is OK, will get clamped
     */
    setVolume(volume) {
        this.#htmlVolume.value = clamp(Math.round(volume * 100), 0, 100);
        this.#htmlVolume.dispatchEvent(new Event('change'));
    }

    /**
     * Apply gain and volume changes
     */
    #applyGain() {
        // If gain node is available, we can immediately set the gain
        // Otherwise, the 'play' event listener will call this method again
        if (!this.#gainNode) {
            console.debug('audiocontext: gainNode not available yet');
            return;
        }
        const gain = parseInt(this.#htmlGain.value);
        const volume = this.#getTransformedVolume();
        console.debug('audiocontext: set gain:', gain, volume, gain * volume);
        // exponential function cannot handle 0 value, so clamp to tiny minimum value instead
        this.#gainNode.gain.exponentialRampToValueAtTime(Math.max(gain * volume, 0.0001), this.#audioContext.currentTime + 0.1);
    }

    #getTransformedVolume() {
        // https://www.dr-lex.be/info-stuff/volumecontrols.html
        return Math.pow(this.getVolume(), 3);
    }

    #updateSliderIcon() {
        const volume = this.#htmlVolume.value;
        this.#htmlVolume.classList.remove('input-volume-high', 'input-volume-medium', 'input-volume-low');
        if (volume > 60) {
            this.#htmlVolume.classList.add('input-volume-high');
        } else if (volume > 30) {
            this.#htmlVolume.classList.add('input-volume-medium');
        } else {
            this.#htmlVolume.classList.add('input-volume-low');
        }
    }
}

const audio = new Audio();
