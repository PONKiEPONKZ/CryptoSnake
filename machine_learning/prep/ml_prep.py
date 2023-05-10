from sklearn.model_selection import train_test_split

def prepare_data(crypto_data_df):
    """
    Prepare data for machine learning.
    
    Parameters:
    -----------
    crypto_data_df : pandas.DataFrame
        DataFrame containing historical cryptocurrency data
        
    Returns:
    --------
    X_train, X_test, y_train, y_test : tuple
        Tuple containing the training and testing data splits
    """
    X = crypto_data_df.drop(["Close"], axis=1)
    y = crypto_data_df["Close"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    return X_train, X_test, y_train, y_test
