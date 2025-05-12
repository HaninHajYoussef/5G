from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
import os
from database import verify_user
import math
from mydatabase import savedb
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
app = FastAPI()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "zayneb9955@gmail.com"  # Remplace par ton email
SMTP_PASSWORD = "iaip whfi jryw zthw"     # Remplace par ton mot de passe d'application (PAS ton mot de passe Gmail direct)


class ForgotPasswordRequest(BaseModel):
    email: str

def send_reset_email(to_email: str):
    """Envoie un email de réinitialisation"""
    message = MIMEMultipart()
    message["From"] = SMTP_USERNAME
    message["To"] = to_email
    message["Subject"] = "Réinitialisation de votre mot de passe"

    body = f"""
    Bonjour,
    Vous avez demandé à réinitialiser votre mot de passe.
    Cliquez sur le lien suivant pour le faire :

    http://votre-site.com/reset-password?email={to_email}

    Merci
    """
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, to_email, message.as_string())
    except Exception as e:
        print(f"Erreur d'envoi d'email : {e}")
        raise HTTPException(status_code=500, detail="Erreur lors de l'envoi de l'email")

@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    # Liste des emails autorisés
    allowed_emails = ["haninhajyoussef1@gmail.com"]

    if request.email not in allowed_emails:
        raise HTTPException(status_code=404, detail="Email non trouvé")

    # Envoie de l'email
    send_reset_email(request.email)
    return {"message": "Email de réinitialisation envoyé avec succès"}


class UserLogin(BaseModel):
    username: str
    password: str

class LinkBudgetParams(BaseModel):
    tx_power: float
    tx_antenna_gain: float
    cable_losses: float
    thermal_noise_density: float
    bandwidth_factor: float
    noise_figure: float
    interference_to_noise: float
    rx_antenna_gain: float
    cable_feeder_loss: float
    diversity_gain: float
    fading_margin_cell_edge: float
    soft_handover_gain: float
    penetration_loss: float
    bs_height: float  
    ue_height: float 
    decay_law: float 

@app.post("/login/")
def login(user: UserLogin):
    if verify_user(user.username, user.password):
        return {"message": "Connexion réussie"}
    raise HTTPException(status_code=401, detail="Identifiants invalides")

@app.post("/calculate/")
def calculate_link_budget(params: LinkBudgetParams):

    d = params.tx_power + params.tx_antenna_gain + params.cable_losses
    n = params.thermal_noise_density + params.noise_figure + params.interference_to_noise + params.bandwidth_factor
    t = n + 2.20  
    x = d + t + params.rx_antenna_gain + params.cable_feeder_loss + params.diversity_gain + params.fading_margin_cell_edge + params.soft_handover_gain + params.penetration_loss
    

    path_loss = x  
    distance = 10 ** ((path_loss + 46.3 + 33.9 * math.log10(params.tx_power) - 13.82 * math.log10(params.bs_height)) / (44.9 - 6.55 * math.log10(params.ue_height)))
    

    fading_margin = params.fading_margin_cell_edge 
    coverage_probability_cell_edge = 0.85 
    fade_margin_whole_cell = fading_margin + 14.46 
   
    surface_cellule = 1.92 * 26 * (distance ** 2)

 
    surface_totale_tozeur = 32 
    nombre_sites_tozeur = surface_totale_tozeur / surface_cellule
    results = {
        "EIRP": d,
        "Noise Density": n,
        "Interference Noise Density": t,
        "Rx Sensitivity": x,
        "Max Path Loss": x,
        "COST 231 Cell Radius (km)": distance,
        "Fade Margin - Whole Cell (dB)": fade_margin_whole_cell,
        "Surface Cellule Tozeur (km²)": surface_cellule,
        "Nombre Sites Tozeur": nombre_sites_tozeur
    }


    savedb("zainebhanin", results)  

    return results
