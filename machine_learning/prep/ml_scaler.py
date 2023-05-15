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

    def unscale_data(self, X_test_scaled, predictions_scaled):
        # Add three empty columns to predictions_scaled
        predictions_scaled = np.column_stack([predictions_scaled, np.zeros((predictions_scaled.shape[0], 3))])
        
        # Unscale the data
        predictions_unscaled = self.scaler.inverse_transform(predictions_scaled)
                
        # Remove the three empty columns from predictions_unscaled
        #predictions_unscaled = predictions_unscaled[:, 0]
        
        return predictions_unscaled