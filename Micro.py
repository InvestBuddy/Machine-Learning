from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import pickle

# Charger le modèle
with open("lsi2.pkl", "rb") as f:
    model = pickle.load(f)

# Initialisation de l'API
app = FastAPI()

# Définition des données d'entrée
class PredictionRequest(BaseModel):
    Genre: int
    Ville: int
    Age: float
    Revenu: float
    Tolérance_au_Risque: int
    Historique_d_Investissement: int
    Objectif_Financier: int
    Secteur_Préféré: str  # Exemple : "actions", "immobilier", etc.
    Fréquence_d_Investissement: int
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
    secteur_prefered_code = {v: k for k, v in secteur_mapping.items()}.get(request.Secteur_Préféré.lower(), -1)

    if secteur_prefered_code == -1:
        print(f"Erreur : Secteur préféré '{request.Secteur_Préféré}' non reconnu.")

    historique_binaire = bin(request.Historique_d_Investissement)[2:].zfill(3)

    input_data = [
        request.Genre, request.Ville, request.Age, request.Revenu / 1000,  # Exemple de normalisation
        request.Tolérance_au_Risque, int(historique_binaire, 2),
        request.Objectif_Financier, secteur_prefered_code,
        request.Fréquence_d_Investissement
    ]

    print(f"Données envoyées au modèle : {input_data}")
    
    predicted_code = model.predict([input_data])[0]
    secteur_recommande = secteur_mapping.get(int(predicted_code), "Inconnu")

    return {
        "domaine_recommandé": secteur_recommande,
        "match_preferred_domain": request.Secteur_Préféré.lower() in [d.lower() for d in request.PreferredDomain],
        "secteur_choisi": request.Secteur_Préféré,
        "domaines_préférés_envoyés": request.PreferredDomain
    }