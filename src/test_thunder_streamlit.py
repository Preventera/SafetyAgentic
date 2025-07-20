import streamlit as st
import sys
import os

# Ajouter le chemin parent pour importer src
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

st.set_page_config(
    page_title="Test Thunder Client",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Test Thunder Client - SafetyGraph")

# Import du module
try:
    from src.api.thunder_integration import add_thunder_client_tab
    
    st.success("✅ Module Thunder Client chargé avec succès !")
    
    # Interface Thunder Client
    add_thunder_client_tab()
    
except Exception as e:
    st.error(f"❌ Erreur : {e}")
    st.write("Détails de l'erreur :", str(e))
    st.write("Chemin actuel :", os.getcwd())
    st.write("Chemins Python :", sys.path)