const VOLUME_HOTKEY_CHANGE = 0.05;


document.addEventListener('keydown', event => {
    // Ignore hotkey when in combination with modifier keys
    if (event.ctrlKey || event.altKey || event.metaKey) {
        return;
    }

    const key = event.key;

    // Don't perform hotkey actions when user is typing in a text field
    // But do still allow escape key
    if (document.activeElement.tagName === 'INPUT' &&
            key !== 'Escape') {
        console.debug('hotkey: ignoring keypress:', key);
        return;
    }

    const keyInt = parseInt(key);
    if (!isNaN(keyInt)) {
        if (keyInt == 0) {
            return;
        }
        const checkboxes = document.getElementById('playlist-checkboxes').getElementsByTagName('input');
        if (checkboxes.length >= keyInt) {
            // Toggle checkbox
            checkboxes[keyInt-1].checked ^= 1;
        }
        savePlaylistState();
    } else if (key === 'p' || key === ' ') {
        const audioElem = player.getAudioElement();
        if (audioElem.paused) {
            audioElem.play();
        } else {
            audioElem.pause();
        }
    } else if (key === 'ArrowLeft') {
        queue.previous();
    } else if (key === 'ArrowRight') {
        queue.next();
    } else if (key == 'ArrowUp') {
        audio.setVolume(audio.getVolume() + VOLUME_HOTKEY_CHANGE);
    } else if (key == 'ArrowDown') {
        audio.setVolume(audio.getVolume() - VOLUME_HOTKEY_CHANGE);
    } else if (key === '.' || key == '>') {
        player.seekRelative(3);
    } else if (key === ',' || key == '<') {
        player.seekRelative(-3);
    } else if (key === 'Escape') {
        windows.closeTop();
    } else if (key == '/') {
        event.preventDefault(true);
        document.getElementById('open-window-search').click();
    } else if (key == "c") {
        queue.clear();
    } else if (key == "l") {
        lyrics.toggleLyrics();
    } else {
        console.debug('hotkey: unhandled keypress:', key);
    }
});
