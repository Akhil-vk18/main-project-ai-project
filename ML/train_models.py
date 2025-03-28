import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, GradientBoostingClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier  # Re-added CatBoost
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load dataset
dataset_path = "./dataset/dataset.csv"
df = pd.read_csv(dataset_path)
df.fillna("", inplace=True)

# Convert all symptom names to lowercase for consistency
df.columns = [col.strip().lower() for col in df.columns]
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.strip().str.lower())

# Convert symptoms to binary encoding
symptom_columns = [col for col in df.columns if "symptom" in col]
encoded_symptoms = pd.get_dummies(df[symptom_columns].stack()).groupby(level=0).sum()

# Save feature names for consistency
trained_features = sorted(encoded_symptoms.columns)
joblib.dump(trained_features, "trained_features.joblib")

# Prepare input (X) and target labels (y)
X = encoded_symptoms.values
y = df["disease"].values

# Encode disease labels as numeric values
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)

# Save the label encoder for decoding predictions
joblib.dump(label_encoder, "label_encoder.joblib")

# Split the dataset for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define models
models = {
    "ExtraTrees": ExtraTreesClassifier(n_estimators=100, random_state=42),
    "RandomForest": RandomForestClassifier(n_estimators=100, random_state=42),
    "GradientBoost": GradientBoostingClassifier(n_estimators=100, random_state=42),
    "LightGBM": LGBMClassifier(n_estimators=100, random_state=42),
    "XGBoost": XGBClassifier(n_estimators=100, use_label_encoder=False, eval_metric="mlogloss"),
    "CatBoost": CatBoostClassifier(iterations=100, verbose=0, random_state=42)  # Re-added CatBoost
}

# Train and save models
for name, model in models.items():
    print(f"Training {name}...")
    model.fit(X_train, y_train)
    joblib.dump(model, f"{name}.joblib")
    print(f"{name} model saved to {name}.joblib")

# Evaluate models
evaluation_results = {name: model.score(X_test, y_test) for name, model in models.items()}

# Save evaluation results to file
with open("model_evaluation.txt", "w") as f:
    for model, score in evaluation_results.items():
        f.write(f"{model}: {score:.4f}\n")
print("Evaluation results saved to model_evaluation.txt")

print("\n✅ Training complete! You can now use these models for predictions.")
