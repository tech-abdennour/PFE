1. Installation des outils


pip install -r requirements.txt

2. Comment lancer le projet
Pour faire fonctionner l'application complete, suivez ces deux etapes :

Etape 1 : Lancer l'API 
L'API permet de faire les calculs de prediction. Dans le terminal, tapez :
python app_api.py

Etape 2 : Lancer le Dashboard 
Ouvrez un deuxieme terminal et lancez l'interface visuelle :
python dashboard.py ou python -m streamlit run dashboard.py

Une fois lance, vous pourrez voir les graphiques dans votre navigateur web.

3. Description des fichiers
Salary_Data (1).csv : Le fichier contenant les donnees de base.

data_processing.py : Le code qui nettoie et prepare les donnees.

salary_model.pkl : Le modele de Machine Learning enregistre.

app_api.py : Le serveur qui envoie les predictions.

dashboard.py : L'interface avec les graphiques (Plotly/Dash).

requirements.txt : La liste des modules a installer.
