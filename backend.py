from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from database import verify_user
import math

app = FastAPI()

# Modèle de connexion utilisateur
class UserLogin(BaseModel):
    username: str
    password: str

# Modèle des paramètres du Link Budget
class LinkBudgetParams(BaseModel):
    tx_power: float
    tx_gain: float
    cable_loss: float
    noise_figure: float
    interference: float
    bandwidth_factor: float
    eb_no: float

# Endpoint de connexion
@app.post("/login/")
def login(user: UserLogin):
    if verify_user(user.username, user.password):
        return {"message": "Connexion réussie"}
    raise HTTPException(status_code=401, detail="Identifiants invalides")

# Endpoint de calcul du Link Budget
@app.post("/calculate/")
def calculate_link_budget(params: LinkBudgetParams):
    eirp = params.tx_power + params.tx_gain - params.cable_loss
    noise_density = -174 + 10 * math.log10(params.bandwidth_factor)
    interference_noise_density = noise_density + params.noise_figure + params.interference
    rx_sensitivity = interference_noise_density + params.eb_no
    
    return {
        "EIRP": eirp,
        "Noise Density": noise_density,
        "Interference Noise Density": interference_noise_density,
        "Rx Sensitivity": rx_sensitivity
    }

# Pour exécuter l'API :
# uvicorn backend:app --reload
