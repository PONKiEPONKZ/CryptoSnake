from sklearn.ensemble import RandomForestClassifier

class RandomForestModel:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)

    def train(self, X_train, y_train):
        # function to train the random forest model using the given training data
        self.model.fit(X_train, y_train)

    def predict(self, X_test):
        # function to predict the output using the trained random forest model and the given test data
        return self.model.predict(X_test)

