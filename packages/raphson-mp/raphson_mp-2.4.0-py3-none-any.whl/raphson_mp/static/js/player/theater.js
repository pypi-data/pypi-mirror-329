class Theater {
    /** @type {HTMLInputElement} */
    #htmlSetting;
    /** @type {HTMLBodyElement} */
    #htmlBody;
    #stillCount = 0;
    #timerId = null;
    #listenerFunction = null;

    constructor() {
        document.addEventListener('DOMContentLoaded', () => {
            this.#htmlSetting = document.getElementById("settings-theater");
            this.#htmlBody = document.getElementsByTagName('body')[0];

            this.#htmlSetting.addEventListener('change', () => this.#onSettingChange());
        });

        eventBus.subscribe(MusicEvent.SETTINGS_LOADED, () => this.#onSettingChange());
    }

    #checkStill() {
        console.debug('theater: timer', this.#stillCount);
        this.#stillCount++;

        if (this.#stillCount > 10) {
            this.#activate();
        }
    }

    #onMove() {
        // if stillCount is not higher than 10, theater mode was never activated
        if (this.#stillCount > 10) {
            this.#deactivate()
        }
        this.#stillCount = 0;
    }

    #onSettingChange() {
        if (this.#timerId) {
            console.debug('theater: unregistered timer');
            clearInterval(this.#timerId);
            this.#timerId = null;
        }

        if (this.#listenerFunction) {
            console.debug('theater: unregistered listener');
            document.removeEventListener('pointermove', this.#listenerFunction);
            this.#listenerFunction = null;
        }

        const theaterModeEnabled = this.#htmlSetting.checked;
        if (theaterModeEnabled) {
            console.debug('theater: registered timer and listener');
            this.#timerId = setInterval(() => this.#checkStill(), 1000);
            this.#listenerFunction = () => this.#onMove();
            document.addEventListener('pointermove', this.#listenerFunction);
            return;
        }
    }

    #activate() {
        this.#htmlBody.classList.add('theater');
    }

    #deactivate() {
        this.#htmlBody.classList.remove('theater');
    }
}

const theater = new Theater();
