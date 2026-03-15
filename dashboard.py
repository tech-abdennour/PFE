import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="PFE - Prédictions Multiples", layout="wide")
st.title("📊 Prédictions Multiples de Salaires")

# 1. Saisie du nombre de personnes
num_predictions = st.number_input("Combien de salaires voulez-vous prédire ?", min_value=1, max_value=20, value=1, step=1)

# Liste pour stocker les années d'expérience saisies
list_years = []

st.subheader(f"Saisie des données pour {num_predictions} profil(s)")

# 2. Création dynamique des champs de saisie
cols = st.columns(3) # Organise les champs sur 3 colonnes pour plus de clarté
for i in range(int(num_predictions)):
    with cols[i % 3]:
        val = st.number_input(f"Années Exp. Personne {i+1}", min_value=0.0, step=0.5, key=f"user_{i}")
        list_years.append(val)

# 3. Bouton pour lancer les prédictions
if st.button("Prédire tous les salaires"):
    predictions = []
    
    try:
        for year in list_years:
            # Appel à l'API Flask pour chaque valeur
            res = requests.post("http://127.0.0.1:5001/api/predict", json={"years": year})
            if res.status_code == 200:
                predictions.append(res.json()['prediction'])
            else:
                predictions.append(0)

        # 4. Création du DataFrame pour l'affichage
        results_df = pd.DataFrame({
            'Personne': [f"P{i+1} ({y} ans)" for i, y in enumerate(list_years)],
            'Salaire Prédit': predictions
        })

        # 5. Affichage du Bar Chart (Matplotlib pour plus de contrôle)
        st.divider()
        st.subheader("Résultats des prédictions")
        
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.bar(results_df['Personne'], results_df['Salaire Prédit'], color='skyblue', edgecolor='navy')
        ax.set_ylabel("Salaire par ans($)")
        ax.set_xlabel("Profils (Années d'expérience)")
        ax.set_title("Comparaison des salaires prédits par le modèle supervisé")
        
        # Ajout des étiquettes de valeur sur les barres
        ax.bar_label(bars, padding=3)
        
        st.pyplot(fig)

        # Affichage du tableau de données
        st.table(results_df)

    except Exception as e:
        st.error(f"Erreur de connexion avec l'API Flask : {e}")