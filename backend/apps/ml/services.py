import os
import pickle
import pandas as pd
import numpy as np
from django.conf import settings

class MLService:
    _model = None
    _scaler = None
    _model_columns = None

    @classmethod
    def _load_artifacts(cls):
        if cls._model is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(base_dir, "artifacts", "best_model.pkl")
            preprocessor_path = os.path.join(base_dir, "artifacts", "preprocessor.pkl")

            try:
                print(f"Loading model from {model_path}...")
                with open(model_path, 'rb') as f:
                    cls._model = pickle.load(f)
                
                print(f"Loading preprocessor from {preprocessor_path}...")
                with open(preprocessor_path, 'rb') as f:
                    cls._scaler, cls._model_columns = pickle.load(f)
                
                print("Artifacts loaded successfully.")
            except Exception as e:
                print(f"Error loading artifacts: {e}")
                cls._model = None
                cls._scaler = None
                cls._model_columns = None

    @classmethod
    def predict(cls, input_data):
        """
        Predict credit risk for input data (dict).
        Returns: {"prediction": int, "probability": float}
        """
        cls._load_artifacts()
        
        if cls._model is None:
            raise Exception("Model not loaded")

        # Convert dict to DataFrame
        df = pd.DataFrame([input_data])
        
        # --- Preprocessing Logic (from Antigravity/predict.py) ---
        
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
        for col in cls._model_columns:
            if col not in df_encoded.columns:
                df_encoded[col] = 0
                
        # Reorder and drop extra columns
        df_encoded = df_encoded[cls._model_columns]
        
        # 4. Scaling
        X_scaled = pd.DataFrame(cls._scaler.transform(df_encoded), columns=df_encoded.columns)
        
        # Predict
        pred = cls._model.predict(X_scaled)[0]
        
        # Probability
        prob = None
        if hasattr(cls._model, "predict_proba"):
            try:
                proba_arr = cls._model.predict_proba(X_scaled)
                if proba_arr.ndim == 2 and proba_arr.shape[1] >= 2:
                    prob = float(proba_arr[:, 1][0])
                else:
                    prob = float(proba_arr[0])
            except Exception:
                pass
                
        return {
            "prediction": int(pred),
            "probability": prob
        }
