import tensorflow as tf
import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, output_size, hidden_layers=[64, 32], learning_rate=0.001):
        self.input_size = input_size
        self.output_size = output_size
        self.hidden_layers = hidden_layers
        self.learning_rate = learning_rate
        self.model = self.create_model()
        
    def create_model(self):
        model = tf.keras.Sequential()
        # Input layer
        model.add(tf.keras.layers.Dense(self.hidden_layers[0], input_shape=(self.input_size,), activation='relu'))
        # Hidden layers
        for i in range(1, len(self.hidden_layers)):
            model.add(tf.keras.layers.Dense(self.hidden_layers[i], activation='relu'))
        # Output layer
        model.add(tf.keras.layers.Dense(self.output_size, activation='linear'))
        # Compile model
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        model.compile(loss='mean_squared_error', optimizer=optimizer)
        return model
        
    def train(self, X_train, y_train, epochs=100, batch_size=32):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=0)

        
    def predict(self, X):
        return self.model.predict(X)
