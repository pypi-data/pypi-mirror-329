// Home button
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('button-home').addEventListener('click', () => window.open('/', '_blank'));
});


// Skip buttons
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById('button-prev').addEventListener('click', () => queue.previous());
    document.getElementById('button-next').addEventListener('click', () => queue.next());
});

// Seek bar
document.addEventListener('DOMContentLoaded', () => {
    const audioElem = player.getAudioElement();
    const seekBar = document.getElementById('seek-bar');
    const seekBarInner =  document.getElementById('seek-bar-inner');
    const textPosition = document.getElementById('seek-bar-text-position')
    const textDuration = document.getElementById('seek-bar-text-duration')

    const onMove = event => {
        audioElem.currentTime = ((event.clientX - seekBar.offsetLeft) / seekBar.offsetWidth) * audioElem.duration;
        event.preventDefault(); // Prevent accidental text selection
    };

    const onUp = () => {
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup', onUp);
    };

    seekBar.addEventListener('mousedown', event => {
        const newTime = ((event.clientX - seekBar.offsetLeft) / seekBar.offsetWidth) * audioElem.duration;
        audioElem.currentTime = newTime;

        // Keep updating while mouse is moving
        document.addEventListener('mousemove', onMove);

        // Unregister events on mouseup event
        document.addEventListener('mouseup', onUp);

        event.preventDefault(); // Prevent accidental text selection
    });

    // Scroll to seek
    seekBar.addEventListener('wheel', event => {
        player.seekRelative(event.deltaY < 0 ? 3 : -3);
    }, {passive: true});

    const updateSeekBar = () => {
        // Save resources updating seek bar if it's not visible
        if (document.visibilityState != 'visible') {
            return;
        }

        var barCurrent;
        var barDuration;
        var barWidth;

        if (isFinite(audioElem.currentTime) && isFinite(audioElem.duration)) {
            barCurrent = durationToString(Math.round(audioElem.currentTime));
            barDuration = durationToString(Math.round(audioElem.duration));
            barWidth = ((audioElem.currentTime / audioElem.duration) * 100) + '%';
        } else {
            barCurrent = '--:--';
            barDuration = '--:--';
            barWidth = 0;
        }

        textPosition.textContent = barCurrent;
        textDuration.textContent = barDuration;
        seekBarInner.style.width = barWidth
    }

    audioElem.addEventListener('durationchange', updateSeekBar);
    audioElem.addEventListener('timeupdate', updateSeekBar);

    // Seek bar is not updated when page is not visible. Immediately update it when the page does become visibile.
    document.addEventListener('visibilitychange', updateSeekBar);
});

// Play and pause buttons
document.addEventListener('DOMContentLoaded', () => {
    const audioElem = player.getAudioElement();
    const pauseButton = document.getElementById('button-pause');
    const playButton = document.getElementById('button-play');

    // Play pause click actions
    pauseButton.addEventListener('click', () => audioElem.pause());
    playButton.addEventListener('click', () => audioElem.play());

    const updateButtons = () => {
        pauseButton.hidden = audioElem.paused;
        playButton.hidden = !audioElem.paused;
    };

    audioElem.addEventListener('pause', updateButtons);
    audioElem.addEventListener('play', updateButtons);

    // Hide pause button on initial page load, otherwise both play and pause will show
    pauseButton.hidden = true;
});

// Handle presence of buttons that perform file actions: dislike, copy, share, edit, delete
document.addEventListener('DOMContentLoaded', () => {
    if (OFFLINE_MODE) {
        return;
    }

    const dislikeButton = document.getElementById('button-dislike');
    const copyButton = document.getElementById('button-copy');
    const shareButton = document.getElementById('button-share');
    const editButton = document.getElementById('button-edit');
    const deleteButton = document.getElementById('button-delete');

    const requiresRealTrack = [dislikeButton, copyButton, shareButton];
    const requiresWriteAccess = [editButton, deleteButton];

    async function updateButtons() {
        const isRealTrack = queue.currentTrack && queue.currentTrack.track;
        for (const button of requiresRealTrack) {
            button.hidden = !isRealTrack;
        }

        const hasWriteAccess = isRealTrack && (await music.playlist(queue.currentTrack.track.playlistName)).write;
        for (const button of requiresWriteAccess) {
            button.hidden = !hasWriteAccess;
        }
    }

    updateButtons();
    eventBus.subscribe(MusicEvent.TRACK_CHANGE, updateButtons);

    // Dislike button
    dislikeButton.addEventListener('click', async () => {
        await queue.currentTrack.track.dislike();
        queue.next();
    });

    // Copy button
    const copyTrack = document.getElementById('copy-track');
    const copyPlaylist = document.getElementById('copy-playlist');
    const copyDoButton = document.getElementById('copy-do-button');
    copyButton.addEventListener('click', () => {
        copyTrack.value = queue.currentTrack.path;
        windows.open('window-copy');
    });
    copyDoButton.addEventListener('click', async () => {
        copyDoButton.disabled = true;
        try {
            await queue.currentTrack.track.copyTo(copyPlaylist.value);
        } catch (err) {
            console.error(err);
            alert('Error: ' + err);
        }
        windows.close('window-copy');
        copyDoButton.disabled = false;
    });

    // Share button is handled by share.js

    // Edit button
    editButton.addEventListener('click', () => {
        if (queue.currentTrack && queue.currentTrack.track) {
            editor.open(queue.currentTrack.track);
        }
    });

    // Delete button
    const deleteSpinner = document.getElementById('delete-spinner');
    deleteButton.addEventListener('click', async () => {
        if (!queue.currentTrack || !queue.currentTrack.track) {
            return;
        }
        deleteSpinner.hidden = false;
        await queue.currentTrack.track.delete();
        queue.next();
        deleteSpinner.hidden = true;
    });
});
