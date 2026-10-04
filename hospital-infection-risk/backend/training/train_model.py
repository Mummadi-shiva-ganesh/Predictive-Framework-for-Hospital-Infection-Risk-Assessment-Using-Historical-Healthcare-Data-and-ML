import os
import json
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score

def train_pipeline():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data", "dataset.csv")
    models_dir = os.path.join(base_dir, "models")
    os.makedirs(models_dir, exist_ok=True)

    print(f"Loading dataset from {data_path}...")
    df = pd.read_csv(data_path)

    # Feature definitions matching exact CSV column names
    num_features = [
        "Age",
        "Surgery_Duration_Min",
        "Blood_Loss_ml",
        "Surgeon_Experience_Years",
        "Room_Temperature_C",
        "Room_Humidity_Pct",
        "Room_CO2_ppm",
        "Room_Occupancy",
        "Cleaning_Interval_Hours",
        "Length_of_Stay_Days"
    ]

    cat_features = [
        "Gender",
        "Surgery_Type",
        "Anesthesia_Type",
        "Pre_Op_Risk_Level",
        "Ventilation_Status"
    ]

    target_col = "Complication_Risk"

    X = df[num_features + cat_features]
    y = df[target_col]

    # Map target string to integer: Low -> 0, Medium -> 1, High -> 2
    target_mapping = {"Low": 0, "Medium": 1, "High": 2}
    y_encoded = y.map(target_mapping)

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )

    # Numerical pipeline with median imputation & scaling
    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler())
    ])

    # Categorical pipeline with most_frequent imputation & one-hot encoding
    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", num_pipeline, num_features),
            ("cat", cat_pipeline, cat_features)
        ]
    )

    print("Fitting preprocessor...")
    X_train_proc = preprocessor.fit_transform(X_train)
    X_test_proc = preprocessor.transform(X_test)

    # Models to evaluate
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42),
        "GradientBoosting": GradientBoostingClassifier(n_estimators=100, max_depth=5, learning_rate=0.1, random_state=42),
        "LogisticRegression": LogisticRegression(max_iter=1000, random_state=42)
    }

    results = {}
    best_model = None
    best_f1 = -1
    best_name = ""

    print("\n--- Model Training & Evaluation ---")
    for name, model in models.items():
        model.fit(X_train_proc, y_train)
        preds = model.predict(X_test_proc)
        probs = model.predict_proba(X_test_proc)

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average="weighted")
        rec = recall_score(y_test, preds, average="weighted")
        f1 = f1_score(y_test, preds, average="weighted")
        auc = roc_auc_score(y_test, probs, multi_class="ovr")

        results[name] = {
            "accuracy": float(acc),
            "precision": float(prec),
            "recall": float(rec),
            "f1_score": float(f1),
            "roc_auc": float(auc)
        }

        print(f"[{name}] Acc: {acc:.4f} | Prec: {prec:.4f} | Rec: {rec:.4f} | F1: {f1:.4f} | AUC: {auc:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model = model
            best_name = name

    print(f"\nBest Model Selected: {best_name} (F1 Score: {best_f1:.4f})")

    # Feature Importance analysis
    cat_encoder = preprocessor.named_transformers_["cat"].named_steps["encoder"]
    cat_feature_names = cat_encoder.get_feature_names_out(cat_features).tolist()
    all_feature_names = num_features + cat_feature_names

    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
        feature_importance_df = pd.DataFrame({
            "feature": all_feature_names,
            "importance": importances
        }).sort_values(by="importance", ascending=False)
        print("\nTop 10 Feature Importances:")
        print(feature_importance_df.head(10).to_string(index=False))

    # Save artifacts
    joblib.dump(best_model, os.path.join(models_dir, "best_model.joblib"))
    joblib.dump(preprocessor, os.path.join(models_dir, "preprocessor.joblib"))
    
    metadata = {
        "best_model_name": best_name,
        "evaluation_metrics": results,
        "num_features": num_features,
        "cat_features": cat_features,
        "encoded_feature_names": all_feature_names,
        "target_mapping": {0: "LOW", 1: "MEDIUM", 2: "HIGH"}
    }

    with open(os.path.join(models_dir, "model_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nArtifacts successfully saved to {models_dir}")

if __name__ == "__main__":
    train_pipeline()
