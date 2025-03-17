import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080"  # Assurez-vous que votre API FastAPI fonctionne sur cette adresse

# Fonction de page de connexion
def login_page():
    st.title("📡 Connexion")

    # Demander à l'utilisateur d'entrer ses identifiants
    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    # Bouton de connexion
    if st.button("Se connecter"):
        # Envoi des identifiants à l'API
        response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})

        if response.status_code == 200:
            st.session_state.authenticated = True  # Stocker l'état de connexion
            st.session_state.username = username  # Stocker le nom d'utilisateur
            st.session_state.page = "calculation"  # Changez l'état de la page à 'calculation'
            st.success("Connexion réussie !")
        else:
            st.error("Identifiants incorrects.")

# Fonction de page de calcul
def calculation_page():
    st.title("📶 Calcul du Link Budget Tunisie Telecom")

    # Vérifier si l'utilisateur est authentifié
    if not st.session_state.get("authenticated", False):
        st.warning("Veuillez vous connecter pour accéder au calcul.")
        st.session_state.page = "login"  # Rediriger vers la page de connexion
        return

    # Formulaire de calcul
    st.header("📡 Paramètres du Link Budget")
    tx_power = st.number_input("Tx Power (dBm)", value=21.0)
    tx_gain = st.number_input("Tx Gain (dBi)", value=0.0)
    cable_loss = st.number_input("Cable Loss (dB)", value=0.0)
    noise_figure = st.number_input("Noise Figure (dB)", value=4.0)
    interference = st.number_input("Interference (dB)", value=6.99)
    bandwidth_factor = st.number_input("Bandwidth Factor", value=53.01)
    eb_no = st.number_input("Eb/No (dB)", value=2.2)

    if st.button("Calculer"):
        payload = {
            "tx_power": tx_power,
            "tx_gain": tx_gain,
            "cable_loss": cable_loss,
            "noise_figure": noise_figure,
            "interference": interference,
            "bandwidth_factor": bandwidth_factor,
            "eb_no": eb_no
        }

        response = requests.post(f"{API_URL}/calculate/", json=payload)

        if response.status_code == 200:
            result = response.json()
            st.success("✅ Calcul réussi !")
            st.write(f"📡 **EIRP** : {result['EIRP']} dBm")
            st.write(f"📡 **Noise Density** : {result['Noise Density']} dBm/Hz")
            st.write(f"📡 **Interference Noise Density** : {result['Interference Noise Density']} dBm")
            st.write(f"📡 **Rx Sensitivity** : {result['Rx Sensitivity']} dBm")
        else:
            st.error("❌ Erreur lors du calcul")

# Configuration initiale
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if 'page' not in st.session_state:
    st.session_state.page = "login"  # Définir la page initiale comme 'login'

# Choisir quelle page afficher en fonction de l'état de la session
if st.session_state.page == "login":
    login_page()
else:
    calculation_page()
