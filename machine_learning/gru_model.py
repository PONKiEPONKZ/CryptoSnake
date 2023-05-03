from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import GRU, Dense

class GRUModel:
    def __init__(self):
        pass

    def train(self, X_train, y_train):
        # define and train the GRU model using the given training data
        model = Sequential()
        model.add(GRU(64, input_shape=(X_train.shape[1], X_train.shape[2]), return_sequences=True))
        model.add(GRU(32, return_sequences=False))
        model.add(Dense(1, activation='sigmoid'))
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        model.fit(X_train, y_train, epochs=50, batch_size=64)

        self.model = model

    def predict(self, X_test):
        # use the trained GRU model to make predictions on the given test data
        return self.model.predict(X_test)

