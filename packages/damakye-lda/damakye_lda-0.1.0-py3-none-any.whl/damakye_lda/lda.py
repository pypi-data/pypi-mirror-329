# damakye_lda/lda.py

import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder

def perform_lda(dataset, target_column):
    """
    Perform LDA on a given dataset.
    
    Args:
    dataset (pd.DataFrame): The input dataset with features and target column.
    target_column (str): The name of the target column for classification.
    
    Returns:
    dict: A dictionary containing the classification report and LDA analysis.
    """
    
    # Separate features (X) and target (y)
    X = dataset.drop(columns=[target_column])
    y = dataset[target_column]
    
    # Encode target variable if categorical
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(y)
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Create an LDA model
    lda = LinearDiscriminantAnalysis()
    
    # Fit the model on training data
    lda.fit(X_train, y_train)
    
    # Predict the results on the test data
    y_pred = lda.predict(X_test)
    
    # Generate classification report
    class_report = classification_report(y_test, y_pred)
    
    # Collect LDA analysis details
    lda_analysis = {
        'mean_vectors': lda.means_,
        'explained_variance_ratio': lda.explained_variance_ratio_,
        'coefficients': lda.coef_
    }
    
    # Return both the classification report and LDA analysis
    return {
        'classification_report': class_report,
        'lda_analysis': lda_analysis
    }
