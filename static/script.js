document.getElementById('qualitySelector').addEventListener('change', function() {
    var videoPlayer = document.getElementById('videoPlayer');
    var videoSource = document.getElementById('videoSource');
    var selectedQuality = this.value;

    var currentTime = videoPlayer.currentTime;
    var isPlaying = !videoPlayer.paused;

    videoPlayer.pause();
    videoSource.src = selectedQuality;
    videoPlayer.load();

    videoPlayer.currentTime = currentTime;
    if (isPlaying) {
        videoPlayer.play();
    }
});