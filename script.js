const video = document.getElementById('videoPlayer');
const playPauseButton = document.getElementById('playPauseButton');
const progressBar = document.getElementById('progressBar');
const timeDisplay = document.getElementById('timeDisplay');
const fullscreenButton = document.getElementById('fullscreenButton');

playPauseButton.addEventListener('click', () => {
  if (video.paused) {
    video.play();
    playPauseButton.textContent = 'Pause';
  } else {
    video.pause();
    playPauseButton.textContent = 'Play';
  }
});

video.addEventListener('timeupdate', () => {
  progressBar.value = (video.currentTime / video.duration) * 100;
  timeDisplay.textContent = formatTime(video.currentTime) + ' / ' + formatTime(video.duration);
});

progressBar.addEventListener('input', () => {
  const seekTime = (progressBar.value / 100) * video.duration;
  video.currentTime = seekTime;
});

function formatTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60);
  return `${minutes}:${secs < 10 ? '0' : ''}${secs}`;
}

fullscreenButton.addEventListener('click', () => {
  if (video.requestFullscreen) {
    video.requestFullscreen();
  } else if (video.webkitRequestFullscreen) {
    video.webkitRequestFullscreen();
  } else if (video.msRequestFullscreen) {
    video.msRequestFullscreen();
  }
});