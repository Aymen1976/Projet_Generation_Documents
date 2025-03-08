import streamlit as st
import requests
import json

# URL de ton API Flask (Remplace par ton URL Ngrok ou celle déployée)
API_URL = "http://localhost:5000/generate"  # Change ceci si tu utilises ngrok ou un déploiement distant

st.title("📄 Générateur de Documents PDF")
st.write("Remplissez les informations ci-dessous pour générer un document PDF.")

# Formulaire utilisateur
titre = st.text_input("Titre du document", "Mon Document")
date = st.date_input("Date du document")
contenu = st.text_area("Contenu", "Écrivez ici le contenu du document...")

if st.button("📄 Générer le PDF"):
    if titre and contenu:
        # Préparation des données JSON pour l'API
        data = {
            "format": "PDF",
            "titre": titre,
            "date": str(date),
            "contenu": contenu
        }
        
        # Envoi de la requête à l'API
        response = requests.post(API_URL, headers={"Content-Type": "application/json"}, data=json.dumps(data))
        
        if response.status_code == 200:
            pdf_url = response.json().get("document_path")
            st.success("✅ PDF généré avec succès !")
            st.markdown(f"[📥 Télécharger le PDF]({pdf_url})", unsafe_allow_html=True)
        else:
            st.error("❌ Une erreur est survenue lors de la génération du PDF.")
    else:
        st.warning("⚠️ Veuillez remplir tous les champs !")

st.write("---")
st.write("🚀 **Déployé avec Streamlit**")
