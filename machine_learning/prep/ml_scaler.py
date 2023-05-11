from sklearn.preprocessing import StandardScaler


class MLScaler:
    def __init__(self):
        self.scaler = StandardScaler()

    def scale_data(self, X_train, X_test):
        self.scaler.fit(X_train)
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def unscale_data(self, scaled_data):
        return self.scaler.inverse_transform(scaled_data)
