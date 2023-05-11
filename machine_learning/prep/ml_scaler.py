from sklearn.preprocessing import StandardScaler
import numpy as np

class MLScaler:
    def __init__(self, remove_negatives=False):
        self.scaler = StandardScaler()
        self.mean_ = None
        self.var_ = None
        self.remove_negatives = remove_negatives
        
    def scale_data(self, X_train, X_test):
        self.scaler.fit(X_train)
        self.mean_ = self.scaler.mean_
        self.var_ = self.scaler.var_
        X_train_scaled = self.scaler.transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        return X_train_scaled, X_test_scaled

    def unscale_data(self, predictions_scaled):
        # Make sure predictions_scaled is a numpy array
        if not isinstance(predictions_scaled, np.ndarray):
            predictions_scaled = np.array(predictions_scaled)
            
        # Unscale the data
        predictions_unscaled = self.scaler.inverse_transform(predictions_scaled)
        
        # Remove any negative values (if applicable)
        if self.remove_negatives:
            predictions_unscaled[predictions_unscaled < 0] = 0
        
        # Ensure that the output is the same shape as the input
        if predictions_scaled.ndim == 1:
            return predictions_unscaled.ravel()
        else:
            return predictions_unscaled
