from fastapi import FastAPI
import pickle
import pandas as pd
from typing import List
from pydantic import BaseModel
import logging

# Configurer les logs
logging.basicConfig(level=logging.INFO)

# Charger le modèle Pickle
with open("model.pkl", "rb") as file:
    model = pickle.load(file)

# Définir l'application FastAPI
app = FastAPI()

# Classe des données d'entrée avec Pydantic pour une validation stricte
class InputFeatures(BaseModel):
    Genre: str
    Ville: str
    Âge: float
    Revenu: float
    Tolérance_au_Risque: str
    Objectif_Financier: str
    Secteur_Préféré: str
    Fréquence_d_Investissement: str
    invest_fundraising: int
    invest_etf: int
    invest_actions: int
    invest_immobilier: int
    invest_obligations: int
    invest_investissement_socialement_responsable: int
    invest_cryptomonnaies: int
    invest_startups: int
    invest_matières_premières: int

# Endpoint pour la prédiction
@app.post("/predict/")
async def predict(features: List[InputFeatures]):
    """
    Reçoit une liste d'objets contenant les features d'entrée.
    """
    # Convertir la liste d'objets Pydantic en DataFrame
    df = pd.DataFrame([feature.dict() for feature in features])

    # Logs pour visualiser les données d'entrée
    logging.info(f"Données reçues : \n{df.head()}")

    # Exemple d'encodage pour les colonnes catégoriques si nécessaire
    try:
        genre_mapping = {"Homme": 0, "Femme": 1}
        risque_mapping = {"faible": 0, "modérée": 1, "élevée": 2}

        # Encoder certaines colonnes (si cela a été fait à l'entraînement)
        df["Genre"] = df["Genre"].map(genre_mapping)
        df["Tolérance_au_Risque"] = df["Tolérance_au_Risque"].map(risque_mapping)

    except KeyError as e:
        return {"error": f"Erreur dans les données envoyées : {e}"}

    # Vérification des colonnes manquantes
    missing_columns = set(model.feature_names_in_) - set(df.columns)
    if missing_columns:
        return {"error": f"Colonnes manquantes : {missing_columns}"}

    # Prédiction
    try:
        predictions = model.predict(df).tolist()  # Convertir en liste pour JSON
        logging.info(f"Prédictions : {predictions}")
        return {"predictions": predictions}
    except Exception as e:
        logging.error(f"Erreur lors de la prédiction : {str(e)}")
        return {"error": f"Erreur lors de la prédiction : {str(e)}"}

# Endpoint de santé pour vérifier si l'API est active
@app.get("/")
async def root():
    return {"message": "API ML fonctionne correctement"}
