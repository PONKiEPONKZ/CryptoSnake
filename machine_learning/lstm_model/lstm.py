import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM

class LSTMModel:
    def __init__(self):
        pass

    def train(self, data, look_back=1):
        # function to train an LSTM model using the given data
        # data should be a 2D numpy array, with each row representing a timestep and each column representing a feature
        # look_back is the number of previous timesteps to use as input for each prediction
        X, Y = [], []
        for i in range(len(data)-look_back):
            X.append(data[i:i+look_back])
            Y.append(data[i+look_back])
        X = np.array(X)
        Y = np.array(Y)
        self.model = Sequential()
        self.model.add(LSTM(50, input_shape=(look_back, X.shape[2])))
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')
        self.model.fit(X, Y, epochs=100, batch_size=32, verbose=2)

    def predict(self, data, look_back=1):
        # function to predict the output using the trained LSTM model and the given data
        # data should be a 2D numpy array, with each row representing a timestep and each column representing a feature
        predictions = []
        for i in range(len(data)-look_back):
            x = data[i:i+look_back]
            x = x.reshape((1, look_back, data.shape[1]))
            prediction = self.model.predict(x, verbose=0)
            predictions.append(prediction[0])
        return np.array(predictions)

