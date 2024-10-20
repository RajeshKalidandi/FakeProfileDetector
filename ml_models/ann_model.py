import tensorflow as tf
from tensorflow.keras import layers, models

def create_ann_model(input_shape):
    model = models.Sequential([
        layers.Dense(64, activation='relu', input_shape=(input_shape,)),
        layers.Dense(32, activation='relu'),
        layers.Dense(16, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def train_ann_model(X_train, y_train, X_val, y_val, epochs=10, batch_size=32):
    input_shape = X_train.shape[1]
    model = create_ann_model(input_shape)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_val, y_val))
    return model, history
