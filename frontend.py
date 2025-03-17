import streamlit as st
import requests

API_URL = "http://127.0.0.1:8080"


st.title("📡 Calcul du Link Budget Tunisie")

# Formulaire de connexion
st.sidebar.title("🔑 Connexion")
username = st.sidebar.text_input("Nom d'utilisateur")
password = st.sidebar.text_input("Mot de passe", type="password")

if st.sidebar.button("Se connecter"):
    response = requests.post(f"{API_URL}/login/", json={"username": username, "password": password})
    if response.status_code == 200:
        st.sidebar.success("Connexion réussie !")
        st.session_state.authenticated = True
    else:
        st.sidebar.error("Échec de connexion")

# Vérification de l'authentification
if not st.session_state.get("authenticated", False):
    st.warning("Veuillez vous connecter pour accéder aux calculs.")
    st.stop()

# Formulaire de calcul du Link Budget
st.header("📶 Paramètres du Link Budget")

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

# Exécuter l'interface avec :
# streamlit run frontend.py
