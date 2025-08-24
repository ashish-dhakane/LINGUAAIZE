import os
import librosa
import numpy as np

def extract_features(file_path, max_len=16):
    audio, sr = librosa.load(file_path, sr=16000)
    mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)
    
    if mfcc.shape[1] < max_len:
        pad_width = max_len - mfcc.shape
        mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)), mode='constant')
    else:
        mfcc = mfcc[:, :max_len]
    
    return mfcc

def load_dataset(commands, base_dir='commands'):
    X, y = [], []
    for idx, cmd in enumerate(commands):
        folder = os.path.join(base_dir, cmd)
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            features = extract_features(file_path)
            X.append(features)
            y.append(idx)
    return np.array(X), np.array(y)

if __name__ == "__main__":
    commands = ['start', 'stop', 'pause']  # Use the commands you recorded
    X, y = load_dataset(commands)
    X = X[..., np.newaxis]  # Adding channel dimension for CNN
    print(f'Dataset loaded: {X.shape}, Labels shape: {y.shape}')
