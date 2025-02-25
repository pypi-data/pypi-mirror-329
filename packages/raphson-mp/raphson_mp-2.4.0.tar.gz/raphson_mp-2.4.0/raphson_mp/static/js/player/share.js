document.addEventListener('DOMContentLoaded', () => {
    if (OFFLINE_MODE) {
        return;
    }

    document.getElementById('button-share').addEventListener('click', async () => {
        if (!queue.currentTrack || !queue.currentTrack.track) {
            // Music not loaded yet
            return;
        }

        const response = await jsonPost('/share/create', {track: queue.currentTrack.track.path});
        const json = await response.json()
        const absoluteShareUrl = new URL('/share/' + json.code, document.location).href;

        const shareData = {url: absoluteShareUrl};

        if (navigator.canShare) {
            if (navigator.canShare(shareData)) {
                navigator.share(shareData);
                return;
            } else {
                console.warn('share: canShare = false');
            }
        } else {
            console.warn('share: Share API is not available');
        }

        window.open(absoluteShareUrl, '_blank');
    });
});
