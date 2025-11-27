import pandas as pd
import numpy as np
import pickle
import os

# Configuration
MODEL_PATH = "best_model.pkl"
PREPROCESSOR_PATH = "preprocessor.pkl"

def load_artifacts():
    """Load the trained model and preprocessors."""
    if not os.path.exists(MODEL_PATH) or not os.path.exists(PREPROCESSOR_PATH):
        raise FileNotFoundError("Model or preprocessor file not found. Please run main.py first.")
        
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
        
    with open(PREPROCESSOR_PATH, 'rb') as f:
        scaler, model_columns = pickle.load(f)
        
    return model, scaler, model_columns

def predict_credit_risk(new_data):
    """
    Predict credit risk for new data.
    
    Args:
        new_data (pd.DataFrame): New data to predict on.
        
    Returns:
        np.array: Predictions (0 for Good, 1 for Bad).
    """
    model, scaler, model_columns = load_artifacts()
    
    # Preprocess new data
    df = new_data.copy()
    
    # Sanitize columns
    df.columns = ["".join (c if c.isalnum() else "_" for c in str(x)) for x in df.columns]
    
    # 1. Handle Missing Values
    cols_to_fill_unknown = ['Saving_accounts', 'Checking_account']
    for col in cols_to_fill_unknown:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            
    # Drop 'Unnamed: 0' or 'Risk' if present
    if 'Unnamed__0' in df.columns:
        df = df.drop(columns=['Unnamed__0'])
    if 'Risk' in df.columns:
        df = df.drop(columns=['Risk'])

    # 2. One-Hot Encoding
    df_encoded = pd.get_dummies(df, drop_first=True)
    
    # 3. Align Columns
    # Add missing columns with 0
    for col in model_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    # Reorder and drop extra columns
    df_encoded = df_encoded[model_columns]
    
    # 4. Scaling
    X_scaled = pd.DataFrame(scaler.transform(df_encoded), columns=df_encoded.columns)
    
    # Predict
    predictions = model.predict(X_scaled)
    return predictions

if __name__ == "__main__":
    # Example usage
    print("Loading sample data for prediction test...")
    try:
        # Load a few rows from original data to test
        sample_df = pd.read_csv("german_credit_data_with_risk.csv").head(5)
        
        # Remove target for simulation
        if 'Risk' in sample_df.columns:
            sample_df = sample_df.drop(columns=['Risk'])
             
        preds = predict_credit_risk(sample_df)
        print(f"Predictions (0=Good, 1=Bad): {preds}")
        
        # Map back to labels
        labels = ['Good' if p == 0 else 'Bad' for p in preds]
        print(f"Labels: {labels}")
        
    except Exception as e:
        print(f"Error during test: {e}")
