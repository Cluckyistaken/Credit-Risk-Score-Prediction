# ml-service/train.py
import argparse
import json
import os
from datetime import datetime

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.metrics import roc_auc_score, accuracy_score, classification_report

from xgboost import XGBClassifier
import joblib

from utils import save_joblib, save_json, ensure_df

DEFAULT_SAMPLE = "sample_data/sample_train.csv"

def build_pipeline(numeric_features, categorical_features, random_state=42):
    # preprocessors
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse=False))
    ])

    preprocessor = ColumnTransformer(transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ], remainder='drop')

    # XGBoost classifier
    xgb = XGBClassifier(
        use_label_encoder=False,
        eval_metric='logloss',
        n_estimators=100,
        max_depth=4,
        random_state=random_state,
        verbosity=0
    )

    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', xgb)
    ])

    return pipeline

def get_feature_names(preprocessor, numeric_features, categorical_features):
    """
    Return transformed feature names (approximate) after ColumnTransformer with OneHotEncoder.
    """
    transformed = []
    # numeric first
    transformed.extend(numeric_features)
    # categorical: get categories from fitted onehot
    cat_transformer = None
    for name, trans, cols in preprocessor.transformers_:
        if name == 'cat':
            cat_transformer = trans
            cat_cols = cols
            break
    if cat_transformer is not None:
        # get categories from the onehot step
        ohe = None
        for step_name, step in cat_transformer.steps:
            if step_name == 'onehot':
                ohe = step
                break
        if ohe is not None:
            categories = ohe.categories_
            for col, cats in zip(cat_cols, categories):
                transformed.extend([f"{col}__{str(c)}" for c in cats])
    return transformed

def train(args):
    data_path = args.data
    df = pd.read_csv(data_path)
    # basic checks
    if 'target' not in df.columns:
        raise ValueError("Training CSV must contain a 'target' column as label")

    # features
    numeric_features = [c for c in df.columns if df[c].dtype.kind in 'biufc' and c != 'target']
    categorical_features = [c for c in df.columns if c not in numeric_features and c != 'target']

    X = df.drop(columns=['target'])
    y = df['target']

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=args.test_size, random_state=args.random_state, stratify=y if len(set(y))>1 else None
    )

    pipeline = build_pipeline(numeric_features, categorical_features, random_state=args.random_state)

    print("Training pipeline...")
    pipeline.fit(X_train, y_train)

    print("Evaluating...")
    preds = pipeline.predict(X_val)
    probs = None
    try:
        probs = pipeline.predict_proba(X_val)[:, 1]
        auc = roc_auc_score(y_val, probs)
    except Exception:
        auc = None

    acc = accuracy_score(y_val, preds)
    clf_report = classification_report(y_val, preds, output_dict=True)

    # save artifacts
    model_artifacts_dir = args.artifacts
    os.makedirs(model_artifacts_dir, exist_ok=True)
    pipeline_path = os.path.join(model_artifacts_dir, "pipeline.joblib")
    model_path = os.path.join(model_artifacts_dir, "model.joblib")

    print(f"Saving pipeline to {pipeline_path}")
    save_joblib(pipeline, pipeline_path)

    # Save raw model (final estimator) as well
    final_estimator = pipeline.named_steps['classifier']
    print(f"Saving raw model to {model_path}")
    save_joblib(final_estimator, model_path)

    # transformed feature names
    transformed_feature_names = get_feature_names(pipeline.named_steps['preprocessor'], numeric_features, categorical_features)
    tf_path = os.path.join(model_artifacts_dir, "transformed_feature_names.json")
    save_json(transformed_feature_names, tf_path)

    # metadata
    metadata = {
        "model_type": "xgboost",
        "training_date": datetime.utcnow().isoformat() + "Z",
        "n_samples": len(df),
        "numeric_features": numeric_features,
        "categorical_features": categorical_features,
        "metrics": {
            "accuracy": float(acc),
            "roc_auc": float(auc) if auc is not None else None,
            "classification_report": clf_report
        },
        "artifact_files": {
            "pipeline": os.path.basename(pipeline_path),
            "raw_model": os.path.basename(model_path),
            "transformed_feature_names": os.path.basename(tf_path)
        }
    }

    metadata_path = os.path.join(model_artifacts_dir, "metadata.json")
    save_json(metadata, metadata_path)

    print("Training complete. Artifacts saved to:", model_artifacts_dir)
    print("Metadata:", metadata_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train ML pipeline and save artifacts")
    parser.add_argument("--data", "-d", default=DEFAULT_SAMPLE, help="Path to training CSV")
    parser.add_argument("--artifacts", "-o", default="model_artifacts", help="Directory to save artifacts")
    parser.add_argument("--random-state", type=int, default=42, dest="random_state")
    parser.add_argument("--test-size", type=float, default=0.2, dest="test_size")
    args = parser.parse_args()
    train(args)
