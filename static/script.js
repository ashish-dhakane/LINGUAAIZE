const recordBtn = document.getElementById('record-btn');
const uploadInput = document.getElementById('upload-audio');
const resultDiv = document.getElementById('result');

recordBtn.onclick = () => {
  // Implement start/stop recording logic (using MediaRecorder API)
  // On stop, send recorded audio data to backend
};

uploadInput.onchange = () => {
  const file = uploadInput.files[0];
  if (file) {
    sendAudio(file);
  }
};

function sendAudio(file) {
  const formData = new FormData();
  formData.append('file', file);

  fetch('/recognize', {
    method: 'POST',
    body: formData
  })
  .then(response => response.json())
  .then(data => {
    resultDiv.textContent = data.command;
  })
  .catch(err => {
    resultDiv.textContent = 'Error recognizing command';
    console.error(err);
  });
}
