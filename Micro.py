from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pickle

# Charger le modèle
with open("projetML.pkl", "rb") as f:
    model = pickle.load(f)

# Initialisation de l'API
app = FastAPI()

# Liste des villes déjà rencontrées (global)
city_index_map = {}

# Liste des domaines possibles pour Investment_History
possible_domains = [
    "actions",
    "immobilier",
    "cryptomonnaies",
    "ETF",
    "obligations",
    "startups",
    "fonds socialement responsables",
    "matières premières",
    "crowdfunding",
    "entreprises locales"
]

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
    "low": 0,
    "medium": 1,
    "high": 2
}

# Mapping pour les objectifs financiers
financial_objective_mapping = {
    "retraite": 0,
    "épargne de sécurité": 1,
    "achat immobilier": 2,
    "éducation des enfants": 3,
    "voyages": 4,
    "épargne de départ": 5,
    "investir dans l'éducation": 6
}

# Mapping pour la fréquence d'investissement
investment_frequency_mapping = {
    "mensuel": 0,
    "trimestriel": 1,
    "annuel": 2
}

# Définition des données d'entrée
class PredictionRequest(BaseModel):
    Gender: str  # "man" ou "woman"
    City: str  # Nom de la ville
    Age: float
    Income: float
    Risk_Tolerance: str  # "low", "medium" ou "high"
    Investment_History: List[str]  # Liste des domaines d'investissement
    Financial_Objective: str  # Exemple : "retraite", "épargne de sécurité", etc.
    Preferred_Sector: str  # Exemple : "actions", "immobilier", etc.
    Investment_Frequency: str  # "mensuel", "trimestriel", "annuel"
    PreferredDomain: List[str]  # Liste des domaines préférés

@app.post("/predict/")
async def predict(request: PredictionRequest):
    # Conversion du genre en entier
    gender_encoded = gender_mapping.get(request.Gender.lower())
    if gender_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Gender '{request.Gender}'. Must be 'man' or 'woman'.")

    # Conversion du nom de la ville en entier
    city = request.City.lower()
    if city not in city_index_map:
        city_index_map[city] = len(city_index_map)  # Assigner un index unique à la ville si elle est inconnue
    city_encoded = city_index_map[city]

    # Conversion de la tolérance au risque en entier
    risk_tolerance_encoded = risk_tolerance_mapping.get(request.Risk_Tolerance.lower())
    if risk_tolerance_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Risk Tolerance '{request.Risk_Tolerance}'.")

    # Conversion de l'objectif financier
    financial_objective_encoded = financial_objective_mapping.get(request.Financial_Objective.lower())
    if financial_objective_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Financial Objective '{request.Financial_Objective}'.")

    # Conversion de la fréquence d'investissement
    investment_frequency_encoded = investment_frequency_mapping.get(request.Investment_Frequency.lower())
    if investment_frequency_encoded is None:
        raise HTTPException(status_code=400, detail=f"Invalid Investment Frequency '{request.Investment_Frequency}'.")

    # Conversion du secteur préféré
    secteur_prefered_code = {v: k for k, v in secteur_mapping.items()}.get(request.Preferred_Sector.lower(), -1)
    if secteur_prefered_code == -1:
        raise HTTPException(status_code=400, detail=f"Invalid Preferred Sector '{request.Preferred_Sector}'.")

    # Création d'un vecteur binaire pour Investment_History
    history_vector = [1 if domain.lower() in [d.lower() for d in request.Investment_History] else 0 for domain in possible_domains]

    # Collecte des domaines ignorés
    ignored_domains = [domain for domain in request.Investment_History if domain.lower() not in [d.lower() for d in possible_domains]]

    if ignored_domains:
        print(f"Warning: The following domains are ignored as they are not valid: {', '.join(ignored_domains)}.")

    # Conversion du vecteur binaire en entier
    investment_history_encoded = int("".join(map(str, history_vector)), 2)

    # Création des données d'entrée pour le modèle
    input_data = [
        gender_encoded, city_encoded, request.Age, request.Income / 1000,
        risk_tolerance_encoded, investment_history_encoded,
        financial_objective_encoded, secteur_prefered_code,
        investment_frequency_encoded
    ]

    print(f"Data sent to the model : {input_data}")
    
    # Prédiction du modèle
    predicted_code = model.predict([input_data])[0]
    secteur_recommande = secteur_mapping.get(int(predicted_code), "Unknown")

    return {
        "recommended_domain": secteur_recommande,
        "match_preferred_domain": request.Preferred_Sector.lower() in [d.lower() for d in request.PreferredDomain],
        "ignored_domains": ignored_domains,
        "selected_sector": request.Preferred_Sector,
        "preferred_domains_sent": request.PreferredDomain,
        "city_index": city_encoded  # Pour voir l'index attribué à la ville
    }
