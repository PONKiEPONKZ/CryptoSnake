from sklearn.tree import DecisionTreeClassifier

class DecisionTree:
    def __init__(self):
        self.model = DecisionTreeClassifier()

    def train(self, data):
        X, y = data['features'], data['labels']
        self.model.fit(X, y)

    def predict(self, data):
        X = data['features']
        return self.model.predict(X)

