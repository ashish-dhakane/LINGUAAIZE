import sounddevice as sd
import numpy as np
import librosa
import tensorflow as tf
import pyttsx3
import keyboard  # For detecting keypress

fs = 16000
duration = 3
max_len = 16
commands = ['start', 'stop', 'pause']

model = tf.keras.models.load_model('voice_command_model.h5')
engine = pyttsx3.init()

def extract_features_live(audio):
    mfcc = librosa.feature.mfcc(y=audio, sr=fs, n_mfcc=13)
    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]
    return mfcc[np.newaxis, ..., np.newaxis]

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_command():
    print("Speak now...")
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    audio = np.squeeze(audio)
    features = extract_features_live(audio)
    prediction = model.predict(features)
    pred_index = np.argmax(prediction)
    confidence = prediction[0][pred_index]
    recognized_command = commands[pred_index]
    
    print(f"Recognized command: '{recognized_command}' with confidence {confidence:.2f}\n")
    
    if recognized_command == 'start':
        speak("Starting now")
    elif recognized_command == 'stop':
        speak("Stopping now")
    elif recognized_command == 'pause':
        speak("Pausing now")
    else:
        speak("Command not recognized")

if __name__ == "__main__":
    print("Starting real-time voice recognition with customized feedback.")
    print("Press 'k' to stop.")

    while True:
        if keyboard.is_pressed('k'):
            print("Stopping program on 'k' key press.")
            break

        recognize_command()
    