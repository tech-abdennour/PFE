import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import time

# Configuration de la page
st.set_page_config(page_title="PFE - Dashboard", layout="centered")

# --- CSS pour style ---
st.markdown("""
    <style>
    .login-box {
        max-width: 350px;
        margin: auto;
        padding: 2rem;
        border-radius: 10px;
        background-color: #f7f7f7;
        box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
        text-align: center;
    }
    .login-box h2 {
        font-size: 1.5rem;
        color: #1877f2; /* bleu Facebook */
        margin-bottom: 1rem;
    }
    .stTextInput > div > div > input {
        font-size: 1rem;
        padding: 0.6rem;
    }
    .stButton button {
        background-color: #1877f2;
        color: white;
        font-weight: bold;
        border-radius: 6px;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGIN ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    st.markdown('<div class="login-box">', unsafe_allow_html=True)
    st.markdown("<h2>Connexion</h2>", unsafe_allow_html=True)

    username = st.text_input("Nom d'utilisateur")
    password = st.text_input("Mot de passe", type="password")

    if st.button("Se connecter"):
        if username == "admin" and password == "1234":
            st.session_state["authenticated"] = True
            st.success("✅ Connexion réussie !")
            st.rerun()
        else:
            st.error("❌ Identifiants incorrects")

    st.markdown('</div>', unsafe_allow_html=True)

else:
    # --- DASHBOARD ---
    st.title("🚀 PFE - Prédictions Multiples de Salaires")

    tab1, tab2 = st.tabs(["📝 Saisie des données", "📊 Résultats"])

    with tab1:
        num_predictions = st.number_input(
            "Combien de salaires voulez-vous prédire ?",
            min_value=1, max_value=20, value=1, step=1
        )

        list_years = []
        st.subheader(f"Saisie des données pour {num_predictions} profil(s)")

        cols = st.columns(3)
        for i in range(int(num_predictions)):
            with cols[i % 3]:
                val = st.number_input(
                    f"Années Exp. Personne {i+1}",
                    min_value=0.0, step=0.5, key=f"user_{i}"
                )
                list_years.append(val)

        if st.button("🎯 Lancer les prédictions"):
            with st.spinner("⏳ Calcul des salaires..."):
                predictions = []
                try:
                    for year in list_years:
                        res = requests.post("http://127.0.0.1:5001/api/predict", json={"years": year})
                        if res.status_code == 200:
                            predictions.append(res.json()['prediction'])
                        else:
                            predictions.append(0)
                        time.sleep(0.3)

                    st.session_state["results_df"] = pd.DataFrame({
                        'Personne': [f"P{i+1} ({y} ans)" for i, y in enumerate(list_years)],
                        'Salaire Prédit': predictions
                    })

                    st.success("✅ Prédictions générées avec succès ! Passez à l'onglet Résultats.")

                except Exception as e:
                    st.error(f"❌ Erreur de connexion avec l'API Flask : {e}")

    with tab2:
        if "results_df" in st.session_state:
            results_df = st.session_state["results_df"]

            st.subheader("📊 Résultats des prédictions")

            fig = px.bar(
                results_df,
                x='Personne',
                y='Salaire Prédit',
                text='Salaire Prédit',
                color='Salaire Prédit',
                color_continuous_scale='Blues',
                title="Comparaison des salaires prédits"
            )
            fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig.update_layout(
                xaxis_title="Profils (Années d'expérience)",
                yaxis_title="Salaire ($)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)"
            )

            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(results_df.style.highlight_max(axis=0, color='lightgreen'), use_container_width=True)
        else:
            st.info("ℹ️ Lancez d'abord les prédictions dans l'onglet Saisie.")

    st.markdown("---")
    st.markdown("👨‍💻 Projet PFE - Dashboard interactif de prédictions de salaires")
