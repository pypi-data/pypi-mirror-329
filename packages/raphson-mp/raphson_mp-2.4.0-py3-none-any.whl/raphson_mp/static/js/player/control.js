controlChannel.registerMessageHandler(ControlCommand.SERVER_PLAY, () => {
    player.getAudioElement().play();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PAUSE, () => {
    player.getAudioElement().pause();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_PREVIOUS, () => {
    queue.previous();
});

controlChannel.registerMessageHandler(ControlCommand.SERVER_NEXT, () => {
    queue.next();
});

async function updateNowPlaying() {
    const audioElem = player.getAudioElement();
    const track = queue.currentTrack && queue.currentTrack.track ? queue.currentTrack.track.path : null;
    const duration = audioElem.duration ? audioElem.duration : (track ? queue.currentTrack.track.duration : null);
    if (duration) {
        const data = {
            track: track,
            paused: audioElem.paused,
            position: audioElem.currentTime,
            duration: duration,
            control: true,
            volume: audio.getVolume(),
        };

        controlChannel.sendMessage(ControlCommand.CLIENT_PLAYING, data);
    }
}

setInterval(updateNowPlaying, 30_000);

document.addEventListener('DOMContentLoaded', () => {
    const audioElem = player.getAudioElement();
    audioElem.addEventListener("play", updateNowPlaying);
    audioElem.addEventListener("pause", updateNowPlaying);
    audioElem.addEventListener("seeked", updateNowPlaying);
});

controlChannel.registerConnectHandler(() => {
    updateNowPlaying();
});
