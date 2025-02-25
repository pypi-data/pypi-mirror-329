const SETTING_ELEMENTS = [
    'settings-queue-size',
    'settings-audio-type',
    'settings-volume',
    'settings-queue-removal-behaviour',
    'settings-download-mode',
    'settings-audio-gain',
    'settings-meme-mode',
    'settings-news',
    'settings-theater',
    'settings-visualiser',
    'settings-lyrics',
];

class Settings {
    constructor() {
        document.addEventListener('DOMContentLoaded', () => {
            SETTING_ELEMENTS.forEach(elem => this.#syncInputWithStorage(elem));
            setTimeout(() => {
                eventBus.publish(MusicEvent.SETTINGS_LOADED);
            }, 0); // publish slightly later, so classes can initialize on DOMContentLoaded first
        });
    }

    #syncInputWithStorage(elemId) {
        const elem = document.getElementById(elemId);
        const isCheckbox = elem.matches('input[type="checkbox"]');

        if (elem.dataset.restore === 'false') {
            return;
        }

        // Initialize input form local storage
        const value = window.localStorage.getItem(elemId);
        if (value !== null) {
            if (isCheckbox) {
                const checked = value === 'true';
                if (elem.checked != checked) {
                    elem.checked = checked;
                }
            } else if (elem.value != value) {
                elem.value = value;
            }
        }

        // If input value is updated, change storage accordingly
        elem.addEventListener('change', event => {
            const value = isCheckbox ? event.target.checked : event.target.value;
            window.localStorage.setItem(elemId, value);
        });
    }

    getTrackDownloadParams() {
        let audioType = document.getElementById('settings-audio-type').value;

        // Legacy
        if (audioType == "mp4_aac") {
            document.getElementById('settings-audio-type').value = "mp3_with_metadata";
        }

        // Safari
        if (audioType.startsWith('webm') &&
                player.getAudioElement().canPlayType("audio/webm;codecs=opus") != "probably" &&
                player.getAudioElement().canPlayType("audio/mpeg;codecs=mp3") == "probably") {
            alert("WEBM/OPUS audio not supported by your browser, audio format has been set to MP3.");
            audioType = "mp3_with_metadata";
        }

        const stream = document.getElementById('settings-download-mode').value == 'stream';
        const memeCover = document.getElementById('settings-meme-mode').checked;
        return [audioType, stream, memeCover];
    }
}

const settings = new Settings();
