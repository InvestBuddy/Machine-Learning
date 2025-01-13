from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pickle

# Charger le modèle
with open("projetML.pkl", "rb") as f:
    model = pickle.load(f)

# Initialisation de l'API
app = FastAPI()

# Définition des données d'entrée
class PredictionRequest(BaseModel):
    Gender: str  # "man" ou "woman"
    City: int
    Age: float
    Income: float
    Risk_Tolerance: str  # "low", "medium" ou "high"
    Investment_History: int
    Financial_Objective: int
    Preferred_Sector: str  # Exemple : "actions", "immobilier", etc.
    Investment_Frequency: int
    PreferredDomain: List[str]  # Liste des domaines préférés

# Mapping des codes numériques des secteurs aux noms des secteurs
secteur_mapping = {
    0: "actions",
    1: "cryptomonnaies",
    2: "ETF",
    3: "immobilier",
    4: "obligations",
    5: "startups"
}

# Mapping pour le genre
gender_mapping = {
    "woman": 0,
    "man": 1
}

# Mapping pour la tolérance au risque
risk_tolerance_mapping = {
    "low": 0,     # Faible tolérance au risque
    "medium": 1,  # Tolérance moyenne
    "high": 2     # Forte tolérance au risque
}

@app.post("/predict/")
async def predict(request: PredictionRequest):
    # Conversion du genre en entier
    gender_encoded = gender_mapping.get(request.Gender.lower())
    if gender_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Gender '{request.Gender}'. Must be 'man' or 'woman'.")

    # Conversion de la tolérance au risque en entier
    risk_tolerance_encoded = risk_tolerance_mapping.get(request.Risk_Tolerance.lower())
    if risk_tolerance_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Risk Tolerance '{request.Risk_Tolerance}'. Must be 'low', 'medium', or 'high'.")

    # Conversion du secteur préféré
    secteur_prefered_code = {v: k for k, v in secteur_mapping.items()}.get(request.Preferred_Sector.lower(), -1)
    if secteur_prefered_code == -1:
        raise HTTPException(status_code=400, detail=f"Invalid Preferred Sector '{request.Preferred_Sector}'.")

    # Encodage binaire de l'historique d'investissement
    historique_binaire = bin(request.Investment_History)[2:].zfill(3)

    # Création des données d'entrée pour le modèle
    input_data = [
        gender_encoded, request.City, request.Age, request.Income / 1000,  # Exemple de normalisation
        risk_tolerance_encoded, int(historique_binaire, 2),
        request.Financial_Objective, secteur_prefered_code,
        request.Investment_Frequency
    ]

    print(f"Data sent to the model : {input_data}")
    
    # Prédiction du modèle
    predicted_code = model.predict([input_data])[0]
    secteur_recommande = secteur_mapping.get(int(predicted_code), "Unknown")

    return {
        "recommended_domain": secteur_recommande,
        "match_preferred_domain": request.Preferred_Sector.lower() in [d.lower() for d in request.PreferredDomain],
        "selected_sector": request.Preferred_Sector,
        "preferred_domains_sent": request.PreferredDomain
    }
