# ml-service/utils.py
import json
import pickle
import os
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from dotenv import load_dotenv

load_dotenv()

def load_pickle(path: str) -> Any:
    with open(path, 'rb') as f:
        return pickle.load(f)

def load_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def ensure_df(data: Any) -> pd.DataFrame:
    """
    Ensure input is a pandas DataFrame.
    Accepts dict, list-of-dicts, pandas.DataFrame.
    """
    if isinstance(data, pd.DataFrame):
        df = data.copy()
    else:
        df = pd.DataFrame(data)
    return df

def preprocess_and_predict(model: Any, scaler: Any, model_columns: List[str], df: pd.DataFrame) -> Dict:
    """
    Preprocess data and predict using the loaded model and scaler.
    Implements the logic from Antigravity/predict.py
    """
    # Preprocess new data
    data = df.copy()
    
    # Sanitize columns
    data.columns = ["".join (c if c.isalnum() else "_" for c in str(x)) for x in data.columns]
    
    # 1. Handle Missing Values
    cols_to_fill_unknown = ['Saving_accounts', 'Checking_account']
    for col in cols_to_fill_unknown:
        if col in data.columns:
            data[col] = data[col].fillna('Unknown')
            
    # Drop 'Unnamed: 0' or 'Risk' if present
    if 'Unnamed__0' in data.columns:
        data = data.drop(columns=['Unnamed__0'])
    if 'Risk' in data.columns:
        data = data.drop(columns=['Risk'])

    # 2. One-Hot Encoding
    df_encoded = pd.get_dummies(data, drop_first=True)
    
    # 3. Align Columns
    # Add missing columns with 0
    for col in model_columns:
        if col not in df_encoded.columns:
            df_encoded[col] = 0
            
    # Reorder and drop extra columns
    df_encoded = df_encoded[model_columns]
    
    # 4. Scaling
    # Transform returns numpy array, wrap back to DF for safety if needed, 
    # but model.predict usually accepts array.
    X_scaled = pd.DataFrame(scaler.transform(df_encoded), columns=df_encoded.columns)
    
    # Predict
    preds = model.predict(X_scaled)
    
    # Try predict_proba
    proba = None
    if hasattr(model, "predict_proba"):
        try:
            proba_arr = model.predict_proba(X_scaled)
            # take probability of positive class if 2d
            if proba_arr.ndim == 2 and proba_arr.shape[1] >= 2:
                proba = proba_arr[:, 1].tolist()
            else:
                proba = proba_arr.tolist()
        except Exception:
            pass
            
    return {
        "predictions": preds.tolist(),
        "probabilities": proba
    }
