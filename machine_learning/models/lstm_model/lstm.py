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
        data = np.array(data[["Open", "High", "Low"]])
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
        self.model.fit(X, Y, epochs=30, batch_size=32, verbose=2)

    def predict(self, data, look_back=1):
        # function to predict the output using the trained LSTM model and the given data
        # data should be a 2D numpy array, with each row representing a timestep and each column representing a feature
        predictions = []
        data_array = np.array(data[["Open", "High", "Low"]])
        for i in range(len(data_array)-look_back):
            x = data_array[i:i+look_back]
            x = x.reshape((1, look_back, data_array.shape[1]))
            prediction = self.model.predict(x, verbose=1)
            predictions.append(prediction[0])
        return np.array(predictions)

    def evaluate(self, data, labels, look_back=1):
    # function to evaluate the performance of the LSTM model on the given data and labels
    # data and labels can be either pandas dataframes or numpy arrays, with each row representing a timestep and each column representing a feature
        if isinstance(data, pd.DataFrame):
            data_array = data[["Open", "High", "Low"]].values
        else:
            data_array = data[:, :3]
        if isinstance(labels, pd.DataFrame):
            labels_array = labels["Close"].values
        else:
            labels_array = labels
        predictions = []
        for i in range(len(data_array)-look_back):
            x = data_array[i:i+look_back]
            x = x.reshape((1, look_back, data_array.shape[1]))
            prediction = self.model.predict(x, verbose=1)
            predictions.append(prediction[0])
        mse = ((np.array(predictions) - labels_array[look_back:])**2).mean()
        return mse

