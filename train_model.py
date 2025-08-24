import numpy as np
import tensorflow as tf
from extract_features import load_dataset

def create_model(input_shape, num_classes):
    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=input_shape),
        tf.keras.layers.MaxPooling2D((2,2)),
        tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2,2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])
    
    model.compile(optimizer='adam',
                  loss='sparse_categorical_crossentropy',
                  metrics=['accuracy'])
    return model

if __name__ == "__main__":
    commands = ['start', 'stop', 'pause']
    X, y = load_dataset(commands)
    X = X[..., np.newaxis]  # Add channel dimension

    model = create_model(X.shape[1:], len(commands))
    model.summary()

    model.fit(X, y, epochs=20, batch_size=4, validation_split=0.2)

    model.save('voice_command_model.h5')
    print("Model saved as 'voice_command_model.h5'")
