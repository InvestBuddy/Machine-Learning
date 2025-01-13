from fastapi import FastAPI
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
    Gender: int
    City: int
    Age: float
    Income: float
    Risk_Tolerance: int
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

@app.post("/predict/")
async def predict(request: PredictionRequest):
    secteur_prefered_code = {v: k for k, v in secteur_mapping.items()}.get(request.Preferred_Sector.lower(), -1)

    if secteur_prefered_code == -1:
        print(f"Error : Preferred Sector '{request.Preferred_Sector}' unrecognized.")

    historique_binaire = bin(request.Investment_History)[2:].zfill(3)

    input_data = [
        request.Gender, request.City, request.Age, request.Income / 1000,  # Exemple de normalisation
        request.Risk_Tolerance, int(historique_binaire, 2),
        request.Financial_Objective, secteur_prefered_code,
        request.Investment_Frequency
    ]

    print(f"Data sent to the model : {input_data}")
    
    predicted_code = model.predict([input_data])[0]
    secteur_recommande = secteur_mapping.get(int(predicted_code), "Unknown")

    return {
        "recommended_domain": secteur_recommande,
        "match_preferred_domain": request.Preferred_Sector.lower() in [d.lower() for d in request.PreferredDomain],
        "selected_sector": request.Preferred_Sector,
        "preferred_domains_sent": request.PreferredDomain
    }