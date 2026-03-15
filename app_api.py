from flask import Flask, jsonify, request
import pandas as pd
import joblib

app = Flask(__name__)

# AJOUTEZ CETTE ROUTE POUR NE PLUS AVOIR "NOT FOUND" SUR LA PAGE D'ACCUEIL
@app.route('/')
def index():
    return "<h1>Serveur Flask en marche !</h1><p>Utilisez <b>/api/data</b> pour voir les données.</p>"

@app.route('/api/data')
def get_data():
    df = pd.read_csv('salaries_with_ml.csv')
    return df.to_json(orient='records')

# Cette route ne fonctionne qu'avec Streamlit (méthode POST)
@app.route('/api/predict', methods=['POST'])
def predict():
    data = request.get_json()
    years = float(data['years'])
    model = joblib.load('salary_model.pkl')
    prediction = model.predict([[years]])[0]
    return jsonify({'prediction': round(prediction, 2)})

if __name__ == '__main__':
    app.run(port=5001, debug=True)