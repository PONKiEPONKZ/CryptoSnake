from sklearn.linear_model import LinearRegression

class RegressionModel:
    def __init__(self):
        self.model = LinearRegression()

    def train(self, X, y):
        # function to train a regression model using the given data
        self.model.fit(X, y)

    def predict(self, X):
        # function to predict the output using the trained regression model and the given data
        return self.model.predict(X)

