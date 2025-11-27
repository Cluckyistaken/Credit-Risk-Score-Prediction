import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xgboost as xgb
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, roc_auc_score, classification_report, confusion_matrix
import pickle
import warnings
import os

warnings.filterwarnings('ignore')

# Configuration
DATA_PATH = "german_credit_data_with_risk.csv"
MODEL_PATH = "best_model.pkl"
EDA_PATH = "eda_outputs"
os.makedirs(EDA_PATH, exist_ok=True)

def load_data(path):
    print(f"Loading data from {path}...")
    try:
        df = pd.read_csv(path)
        # Sanitize column names
        df.columns = ["".join (c if c.isalnum() else "_" for c in str(x)) for x in df.columns]
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File {path} not found.")
        return None

def preprocess_data(df):
    print("Starting data preprocessing...")
    
    # 1. Handle Missing Values
    # Specific rule: Treat NaNs in checking/savings as "Unknown"
    # Note: Column names were sanitized. 'Saving accounts' -> 'Saving_accounts', 'Checking account' -> 'Checking_account'
    
    cols_to_fill_unknown = ['Saving_accounts', 'Checking_account']
    for col in cols_to_fill_unknown:
        if col in df.columns:
            df[col] = df[col].fillna('Unknown')
            print(f"Filled NaNs in {col} with 'Unknown'")
            
    # Drop 'Unnamed: 0' if exists (often index)
    if 'Unnamed__0' in df.columns:
        df = df.drop(columns=['Unnamed__0'])
    
    # 2. Target Encoding
    # Target is 'Risk'. Map 'bad' -> 1, 'good' -> 0
    if 'Risk' in df.columns:
        print("Encoding target 'Risk'...")
        # Check unique values to be sure
        unique_vals = df['Risk'].unique()
        print(f"Target values: {unique_vals}")
        
        # Map: bad -> 1, good -> 0
        df['Risk'] = df['Risk'].apply(lambda x: 1 if str(x).lower() == 'bad' else 0)
        y = df['Risk']
        X = df.drop(columns=['Risk'])
    else:
        raise ValueError("Target column 'Risk' not found!")

    # 3. Feature Encoding (One-Hot Encoding)
    print("Performing One-Hot Encoding...")
    X = pd.get_dummies(X, drop_first=True)
    
    # 4. Scaling
    print("Scaling features...")
    scaler = StandardScaler()
    X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    
    print(f"Preprocessing completed. Features shape: {X_scaled.shape}")
    return X_scaled, y, scaler

def train_models(X_train, y_train):
    print("Training models...")
    models = {}
    
    # 1. RandomForest
    print("Training RandomForest...")
    rf_clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
    rf_clf.fit(X_train, y_train)
    models['RandomForest'] = rf_clf
    
    # 2. XGBoost
    print("Training XGBoost...")
    xgb_clf = xgb.XGBClassifier(random_state=42, use_label_encoder=False, eval_metric='logloss')
    xgb_clf.fit(X_train, y_train)
    models['XGBoost'] = xgb_clf
    
    return models

def evaluate_models(models, X_test, y_test):
    print("Evaluating models...")
    results = []
    
    for name, model in models.items():
        y_pred = model.predict(X_test)
        y_prob = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
        
        acc = accuracy_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_prob) if y_prob is not None else 0
        
        print(f"\n--- {name} ---")
        print(f"Accuracy: {acc:.4f}")
        print(f"AUC-ROC: {auc:.4f}")
        print("Classification Report (Target: 1=Bad, 0=Good):")
        print(classification_report(y_test, y_pred, target_names=['Good', 'Bad']))
        
        results.append({
            'Model': name,
            'Accuracy': acc,
            'AUC-ROC': auc
        })
        
        # Confusion Matrix
        cm = confusion_matrix(y_test, y_pred)
        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Reds', xticklabels=['Good', 'Bad'], yticklabels=['Good', 'Bad'])
        plt.title(f'Confusion Matrix - {name}')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.savefig(f"{EDA_PATH}/cm_{name}_retrained.png")
        plt.close()

    return pd.DataFrame(results)

def main():
    # 1. Load Data
    df = load_data(DATA_PATH)
    if df is None:
        return

    # 2. Preprocessing
    X, y, scaler = preprocess_data(df)
    
    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 4. Train Models
    models = train_models(X_train, y_train)
    
    # 5. Evaluation
    results_df = evaluate_models(models, X_test, y_test)
    print("\nModel Comparison:")
    print(results_df)
    results_df.to_csv("model_comparison_retrained.csv", index=False)
    
    # 6. Select Best Model (based on Accuracy as requested > 70%)
    best_model_name = results_df.sort_values(by='Accuracy', ascending=False).iloc[0]['Model']
    best_model = models[best_model_name]
    best_acc = results_df[results_df['Model'] == best_model_name]['Accuracy'].values[0]
    
    print(f"\nBest Model Selected: {best_model_name} with Accuracy: {best_acc:.4f}")
    
    if best_acc < 0.70:
        print("WARNING: Accuracy is below 70%. Consider tuning or more feature engineering.")
    
    # 7. Save Best Model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(best_model, f)
    print(f"Best model saved to {MODEL_PATH}")
    
    # Save scaler (encoders are implicit in OneHot, but we need to handle columns in predict)
    # For OneHot, we need to save the list of columns after training to align new data
    with open("preprocessor.pkl", 'wb') as f:
        pickle.dump((scaler, X.columns.tolist()), f) # Saving columns list instead of encoders

if __name__ == "__main__":
    main()
