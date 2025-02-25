document.addEventListener('DOMContentLoaded', () => {
    if (OFFLINE_MODE) {
        return;
    }

    /** @type {HTMLButtonElement} */
    const addButton = document.getElementById('online-add');
    /** @type {HTMLInputElement} */
    const urlInput = document.getElementById('online-url');

    addButton.addEventListener('click', async () => {
        windows.close('window-online');
        const track = await music.downloadTrackFromWeb(urlInput.value);
        queue.add(track, true);
    })
});
