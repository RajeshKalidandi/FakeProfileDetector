import tensorflow as tf
from tensorflow.keras import layers, models

def create_rnn_model(input_shape, vocab_size):
    model = models.Sequential([
        layers.Embedding(vocab_size, 64, input_length=input_shape[0]),
        layers.LSTM(64, return_sequences=True),
        layers.LSTM(32),
        layers.Dense(32, activation='relu'),
        layers.Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam',
                  loss='binary_crossentropy',
                  metrics=['accuracy'])
    return model

def train_rnn_model(X_train, y_train, X_val, y_val, vocab_size, epochs=10, batch_size=32):
    input_shape = X_train.shape[1:]
    model = create_rnn_model(input_shape, vocab_size)
    history = model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size,
                        validation_data=(X_val, y_val))
    return model, history
