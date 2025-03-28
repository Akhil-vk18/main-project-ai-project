from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pickle
import numpy as np
import pandas as pd
import os
import json
from treatment.models import *
from collections import Counter
# Load the model
import joblib

models = {
    "ExtraTrees": joblib.load("./ML/ExtraTrees.joblib"),
    "RandomForest": joblib.load("./ML/RandomForest.joblib"),
    "GradientBoost": joblib.load("./ML/GradientBoost.joblib"),
    "LightGBM": joblib.load("./ML/LightGBM.joblib"),
    "XGBoost": joblib.load("./ML/XGBoost.joblib")
}

# Load label encoder for decoding predictions
label_encoder = joblib.load("./ML/label_encoder.joblib")

# Load feature names for input consistency
trained_features = joblib.load("./ML/trained_features.joblib")
df = pd.read_csv("C:/Users/akhil/Desktop/freak/main project/health_monitoring/medical/dataset/dataset.csv")
df.fillna("", inplace=True)

desc = pd.read_csv("C:/Users/akhil/Desktop/freak/main project/health_monitoring/medical/dataset/symptom_Description.csv")
prec = pd.read_csv("C:/Users/akhil/Desktop/freak/main project/health_monitoring/medical/dataset/symptom_precaution.csv")
# Normalize dataset columns
df.columns = [col.strip().lower() for col in df.columns]
df.iloc[:, 1:] = df.iloc[:, 1:].apply(lambda x: x.str.strip().str.lower())


# Define the symptoms and diseases
diseases = ['(vertigo) Paroymsal  Positional Vertigo', 'AIDS', 'Acne', 'Alcoholic hepatitis', 'Allergy', 'Arthritis', 
            'Bronchial Asthma', 'Cervical spondylosis', 'Chicken pox', 'Chronic cholestasis', 'Common Cold', 'Dengue', 
            'Diabetes', 'Dimorphic hemmorhoids(piles)', 'Drug Reaction', 'Fungal infection', 'GERD', 'Gastroenteritis', 
            'Heart attack', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Hypertension', 'Hyperthyroidism', 
            'Hypoglycemia', 'Hypothyroidism', 'Impetigo', 'Jaundice', 'Malaria', 'Migraine', 'Osteoarthristis', 
            'Paralysis (brain hemorrhage)', 'Peptic ulcer diseae', 'Pneumonia', 'Psoriasis', 'Tuberculosis', 'Typhoid', 
            'Urinary tract infection', 'Varicose veins', 'hepatitis A']

symptoms = [
    'itching', 'skin_rash', 'nodal_skin_eruptions', 'continuous_sneezing', 'shivering', 'chills', 'joint_pain',
    'stomach_pain', 'acidity', 'ulcers_on_tongue', 'muscle_wasting', 'vomiting', 'burning_micturition', 'fatigue',
    'weight_gain', 'anxiety', 'cold_hands_and_feets', 'mood_swings', 'weight_loss', 'restlessness', 'lethargy',
    'patches_in_throat', 'irregular_sugar_level', 'cough', 'high_fever', 'sunken_eyes', 'breathlessness',
    'sweating', 'dehydration', 'indigestion', 'headache', 'yellowish_skin', 'dark_urine', 'nausea',
    'loss_of_appetite', 'pain_behind_the_eyes', 'back_pain', 'constipation', 'abdominal_pain', 'diarrhoea',
    'mild_fever', 'yellow_urine', 'yellowing_of_eyes', 'acute_liver_failure', 'fluid_overload', 'swelling_of_stomach',
    'swelled_lymph_nodes', 'malaise', 'blurred_and_distorted_vision', 'phlegm', 'throat_irritation', 'redness_of_eyes',
    'sinus_pressure', 'runny_nose', 'congestion', 'chest_pain', 'weakness_in_limbs', 'fast_heart_rate',
    'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'neck_pain',
    'dizziness', 'cramps', 'bruising', 'obesity', 'swollen_legs', 'swollen_blood_vessels', 'puffy_face_and_eyes',
    'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'excessive_hunger', 'extra_marital_contacts',
    'drying_and_tingling_lips', 'slurred_speech', 'knee_pain', 'hip_joint_pain', 'muscle_weakness', 'stiff_neck',
    'swelling_joints', 'movement_stiffness', 'spinning_movements', 'loss_of_balance', 'unsteadiness',
    'weakness_of_one_body_side', 'loss_of_smell', 'bladder_discomfort', 'continuous_feel_of_urine',
    'passage_of_gases', 'internal_itching', 'toxic_look_(typhos)', 'depression', 'irritability', 'muscle_pain',
    'altered_sensorium', 'red_spots_over_body', 'belly_pain', 'abnormal_menstruation', 'watering_from_eyes',
    'increased_appetite', 'polyuria', 'family_history', 'mucoid_sputum', 'rusty_sputum', 'lack_of_concentration',
    'visual_disturbances', 'receiving_blood_transfusion', 'receiving_unsterile_injections', 'coma',
    'stomach_bleeding', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'blood_in_sputum',
    'prominent_veins_on_calf', 'palpitations', 'painful_walking', 'pus_filled_pimples', 'blackheads', 'scurring',
    'skin_peeling', 'silver_like_dusting', 'small_dents_in_nails', 'inflammatory_nails', 'blister', 'red_sore_around_nose',
    'yellow_crust_ooze', 'prognosis', 'skin_rash', 'pus_filled_pimples', 'mood_swings', 'weight_loss', 'fast_heart_rate',
    'excessive_hunger', 'muscle_weakness', 'abnormal_menstruation', 'muscle_wasting', 'patches_in_throat',
    'high_fever', 'extra_marital_contacts', 'yellowish_skin', 'loss_of_appetite', 'abdominal_pain', 'yellowing_of_eyes',
    'chest_pain', 'loss_of_balance', 'lack_of_concentration', 'blurred_and_distorted_vision', 'drying_and_tingling_lips',
    'slurred_speech', 'stiff_neck', 'swelling_joints', 'painful_walking', 'dark_urine', 'yellow_urine',
    'receiving_blood_transfusion', 'receiving_unsterile_injections', 'visual_disturbances', 'burning_micturition',
    'bladder_discomfort', 'foul_smell_of_urine', 'continuous_feel_of_urine', 'irregular_sugar_level',
    'increased_appetite', 'joint_pain', 'skin_peeling', 'small_dents_in_nails', 'inflammatory_nails',
    'swelling_of_stomach', 'distention_of_abdomen', 'history_of_alcohol_consumption', 'fluid_overload',
    'pain_during_bowel_movements', 'pain_in_anal_region', 'bloody_stool', 'irritation_in_anus', 'acute_liver_failure',
    'stomach_bleeding', 'back_pain', 'weakness_in_limbs', 'neck_pain', 'mucoid_sputum', 'mild_fever', 'muscle_pain',
    'family_history', 'continuous_sneezing', 'watering_from_eyes', 'rusty_sputum', 'weight_gain', 'puffy_face_and_eyes',
    'enlarged_thyroid', 'brittle_nails', 'swollen_extremeties', 'swollen_legs', 'prominent_veins_on_calf',
    'stomach_pain', 'spinning_movements', 'sunken_eyes', 'silver_like_dusting', 'swelled_lymph_nodes',
    'blood_in_sputum', 'swollen_blood_vessels', 'toxic_look_(typhos)', 'belly_pain', 'throat_irritation',
    'redness_of_eyes', 'sinus_pressure', 'runny_nose', 'loss_of_smell', 'passage_of_gases', 'cold_hands_and_feets',
    'weakness_of_one_body_side', 'altered_sensorium', 'nodal_skin_eruptions', 'red_sore_around_nose', 'yellow_crust_ooze',
    'ulcers_on_tongue', 'spotting_urination', 'pain_behind_the_eyes', 'red_spots_over_body', 'internal_itching'
]

high_risk_diseases = {"Heart attack", "AIDS", "Hepatitis B", "Hepatitis C", "Hepatitis D", "Hepatitis E","Paralysis (brain hemorrhage)","(vertigo) Paroymsal  Positional Vertigo"}

# Load the description and precaution datasets




def home(request):
    return render(request, 'web.html')  # Assuming you have a web.html template
def pred(request):
    return render(request, 'predict.html')  # Assuming you have a web.html template



symptom_to_diseases = {}
for _, row in df.iterrows():
    disease = row["disease"]
    symptoms = row[1:].dropna().values  # Get symptoms for each disease
    for symptom in symptoms:
        symptom_to_diseases.setdefault(symptom, []).append(disease)





def create_symptom_vector(selected_symptoms):
    t = pd.Series([0] * len(trained_features), index=trained_features)
    for symptom in selected_symptoms:
        if symptom in t.index:
            t.loc[symptom] = 1
    return t.to_numpy().reshape(1, -1)

# Function to get top 5 predictions per model
def predict_top_5(model, features, num_symptoms, valid_diseases):
    probs = model.predict_proba(features)[0]  # Get probability scores
    top10_indices = np.argsort(probs)[-10:][::-1]  # Get top 10 diseases
    top10_diseases = label_encoder.inverse_transform(top10_indices)  # Convert indices to names

    # Filter by dataset-matched diseases
    filtered_diseases = [d for d in top10_diseases if d in valid_diseases]

    # If only 1 symptom, remove high-risk diseases
    if num_symptoms == 1:
        filtered_diseases = [d for d in filtered_diseases if d not in high_risk_diseases]

    return filtered_diseases[:5]  # Return top 5 diseases

# Function to prioritize dataset-matched diseases
def prioritize_by_dataset(all_predictions, selected_symptoms):
    dataset_matched_diseases = set()
    for symptom in selected_symptoms:
        if symptom in symptom_to_diseases:
            dataset_matched_diseases.update(symptom_to_diseases[symptom])

    filtered_counts = {disease: count for disease, count in all_predictions.items() if disease in dataset_matched_diseases}

    return Counter(filtered_counts).most_common(5)
@csrf_exempt
def predict_disease_view(request):
    if request.method == 'POST':
        selected_symptoms = json.loads(request.POST.get('selected_symptoms', '[]'))
        selected_symptoms = [s.lower().strip() for s in selected_symptoms]

        valid_diseases = set()
        for symptom in selected_symptoms:
            if symptom in symptom_to_diseases:
                valid_diseases.update(symptom_to_diseases[symptom])

        if not valid_diseases:
            return JsonResponse({'predictions': []})

        features = create_symptom_vector(selected_symptoms)
        num_symptoms = sum(features[0])

        all_predictions = Counter()
        for name, model in models.items():
            top5 = predict_top_5(model, features, num_symptoms, valid_diseases)
            all_predictions.update(top5)
            print(f"🔹 {name}: {top5}")

        final_top5 = prioritize_by_dataset(all_predictions, selected_symptoms) or []

        if not final_top5:
            return JsonResponse({'predictions': []})

        final_top5 = sorted(final_top5, key=lambda x: (x[1] / len(models)) * 100, reverse=True)

        disease, count = final_top5[0]
        probability = (count / len(models)) * 100

        description = (
            desc.loc[desc['Disease'] == disease, 'Description'].iloc[0]
            if disease in desc["Disease"].unique() else "No description available"
        )

        precautions = []
        if disease in prec["Disease"].unique():
            c = np.where(prec['Disease'] == disease)[0][0]
            for j in range(1, len(prec.iloc[c])):
                precautions.append(prec.iloc[c, j])

        treatment_list = []
        treatments = Treatments.objects.filter(disease__disease=disease)
        for treatment in treatments:
            treatment_list.append({
                'treatment_name': treatment.treatment_name,
                'details': treatment.details,
                'doc_id': treatment.dr_id.id,
                'doctor_username': treatment.dr_id.username,
                'doctor_link': f"/vw_doc_details/{treatment.dr_id.id}/"
            })

        prediction = {
            'disease': disease,
            'probability': float(probability),
            'description': description,
            'precautions': precautions,
            'treatment_list': treatment_list
        }

        return JsonResponse({'predictions': [prediction]})

    return render(request, 'predict.html')
