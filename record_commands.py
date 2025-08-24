import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wav
import os

def record_command(command_name, duration=3, fs=16000, n_samples=5):
    """
    Records 'n_samples' audio clips of 'duration' seconds each for a given command.
    Saves them in folders named after commands.
    After each recording, waits for user to press Enter to continue.
    """
    os.makedirs(f'commands/{command_name}', exist_ok=True)
    print(f"Recording samples for command: '{command_name}' with duration {duration} seconds each.")
    
    for i in range(n_samples):
        input(f"\nSample {i+1}/{n_samples}: Press Enter and then speak your command '{command_name}' clearly.")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
        sd.wait()  # Wait until recording finishes
        filename = f'commands/{command_name}/{command_name}_{i+1}.wav'
        wav.write(filename, fs, np.squeeze(audio))
        print(f"Saved sample {i+1} as {filename}")

if __name__ == "__main__":
    commands = ['start', 'stop', 'pause']  # Modify commands here
    for cmd in commands:
        record_command(cmd)
