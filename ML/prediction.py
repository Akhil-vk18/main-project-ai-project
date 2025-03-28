import joblib
import numpy as np
import pandas as pd
from collections import Counter

# Load trained models
models = {
    "ExtraTrees": joblib.load("ExtraTrees.joblib"),
    "RandomForest": joblib.load("RandomForest.joblib"),
    "GradientBoost": joblib.load("GradientBoost.joblib"),
    "LightGBM": joblib.load("LightGBM.joblib"),
    "XGBoost": joblib.load("XGBoost.joblib"),
    "CatBoost": joblib.load("CatBoost.joblib")
}

# Load label encoder for decoding predictions
label_encoder = joblib.load("label_encoder.joblib")

# Load feature names for input consistency
trained_features = joblib.load("trained_features.joblib")

# Load dataset to map symptoms to diseases
df = pd.read_csv("./dataset/dataset.csv")
df.fillna("", inplace=True)

# Normalize dataset columns
df.columns = [col.strip().lower() for col in df.columns]
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.strip().str.lower())

# Create symptom-to-disease mapping from dataset
symptom_to_diseases = {}
for _, row in df.iterrows():
    disease = row["disease"]
    symptoms = row[1:].dropna().values  # Get symptoms for each disease
    for symptom in symptoms:
        symptom_to_diseases.setdefault(symptom, []).append(disease)

# Function to create symptom vector
def create_symptom_vector(selected_symptoms):
    t = pd.Series([0] * len(trained_features), index=trained_features)
    for symptom in selected_symptoms:
        if symptom in t.index:
            t.loc[symptom] = 1
    return t.to_numpy().reshape(1, -1)

# High-risk diseases (shouldn't be predicted from a single symptom)
high_risk_diseases = {"Heart attack", "AIDS", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E","Paralysis (brain hemorrhage)","(vertigo) Paroymsal  Positional Vertigo"}

# Function to get top disease predictions per model
def predict_top_5(model, features, num_symptoms, valid_diseases):
    probs = model.predict_proba(features)[0]  # Get probability scores
    top10_indices = np.argsort(probs)[-10:][::-1]  # Get indices of top 10 diseases
    top10_diseases = label_encoder.inverse_transform(top10_indices)  # Convert to disease names

    # Filter by dataset-matched diseases
    filtered_diseases = [d for d in top10_diseases if d in valid_diseases]

    # If only 1 symptom is provided, remove high-risk diseases
    if num_symptoms == 1:
        filtered_diseases = [d for d in filtered_diseases if d not in high_risk_diseases]

    return filtered_diseases[:5]  # Return top 5 diseases

# **NEW LOGIC**: Prioritize dataset-matched diseases
def prioritize_by_dataset(all_predictions, selected_symptoms):
    # Get only diseases linked to the entered symptoms
    dataset_matched_diseases = set()
    for symptom in selected_symptoms:
        if symptom in symptom_to_diseases:
            dataset_matched_diseases.update(symptom_to_diseases[symptom])

    # Re-rank diseases based on dataset presence
    filtered_counts = {disease: count for disease, count in all_predictions.items() if disease in dataset_matched_diseases}

    # Get top 5 diseases from filtered list
    return Counter(filtered_counts).most_common(5)

# Function to predict disease based on symptoms
def predict_disease(selected_symptoms):
    print(f"\n🩺 Predicting disease for symptoms: {selected_symptoms}")
    
    # Normalize symptoms to lowercase
    selected_symptoms = [s.lower().strip() for s in selected_symptoms]

    # Find valid diseases from dataset
    valid_diseases = set()
    for symptom in selected_symptoms:
        if symptom in symptom_to_diseases:
            valid_diseases.update(symptom_to_diseases[symptom])

    print(f"🔍 Matched diseases from dataset: {valid_diseases}")  # Debugging

    if not valid_diseases:
        print("❌ No matching diseases found in dataset for these symptoms.")
        return

    # Create symptom vector
    features = create_symptom_vector(selected_symptoms)
    num_symptoms = sum(features[0])  # Count number of entered symptoms

    # Get predictions from models
    all_predictions = Counter()
    
    for name, model in models.items():
        top5 = predict_top_5(model, features, num_symptoms, valid_diseases)
        all_predictions.update(top5)
        print(f"🔹 {name}: {top5}")

    # **NEW STEP**: Prioritize diseases based on dataset symptom matching
    final_top5 = prioritize_by_dataset(all_predictions, selected_symptoms)

    print("\n✅ Final Top 5 Predicted Diseases (Filtered & Ranked by Dataset Match):")
    for disease, count in final_top5:
        print(f"   - {disease} (Predicted by {count} models)")

# Example: Predict disease for given symptoms
if __name__ == "__main__":
    user_symptoms = ["vomiting","sunken_eyes","breathlessness","chest_pain"]  # Change symptoms here
    predict_disease(user_symptoms)
