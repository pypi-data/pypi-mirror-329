window.addEventListener("pagehide", () => {
    if (OFFLINE_MODE) {
        return;
    }

    controlChannel.sendStopSignal();
});
