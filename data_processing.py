import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import joblib

# Configuration du style
plt.style.use('default')
sns.set_palette("husl")

# 1. Chargement des données
df = pd.read_csv('salaries_with_ml.csv')

# 2. Entraînement du modèle
X = df[['YearsExperience']]
y = df['Salary']
model = LinearRegression()
model.fit(X, y)

# 3. Prédictions
df['Salary_Predicted'] = model.predict(X)

# 4. Sauvegardes
joblib.dump(model, 'salary_model.pkl')
df.to_csv('salaries_with_ml.csv', index=False)

# 5. Création du graphique
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Graphique 1: Nuage de points + ligne de régression
axes[0].scatter(df['YearsExperience'], df['Salary'], 
                color='blue', alpha=0.6, s=100, label='Données réelles')
axes[0].plot(df['YearsExperience'], df['Salary_Predicted'], 
             color='red', linewidth=2, label='Régression linéaire')
axes[0].set_xlabel('Années d\'expérience', fontsize=12)
axes[0].set_ylabel('Salaire ($)', fontsize=12)
axes[0].set_title('📊 Modèle de Prédiction des Salaires\nRégression Linéaire', fontsize=14, fontweight='bold')
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Ajout des coefficients
equation = f'y = {model.coef_[0]:.2f}x + {model.intercept_:.2f}'
axes[0].text(0.05, 0.95, f'Équation: {equation}', 
             transform=axes[0].transAxes, fontsize=11,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

# Graphique 2: Comparaison réel vs prédit
axes[1].scatter(df['Salary'], df['Salary_Predicted'], 
                color='green', alpha=0.6, s=100)
axes[1].plot([df['Salary'].min(), df['Salary'].max()], 
             [df['Salary'].min(), df['Salary'].max()], 
             'r--', linewidth=2, label='Prédiction parfaite')
axes[1].set_xlabel('Salaire réel ($)', fontsize=12)
axes[1].set_ylabel('Salaire prédit ($)', fontsize=12)
axes[1].set_title('📈 Réel vs Prédit', fontsize=14, fontweight='bold')
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3)

# Calcul du R² pour le titre
r2_score = model.score(X, y)
fig.suptitle(f'Modèle de Régression Linéaire - R² = {r2_score:.3f}', 
             fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('modele_regression_lineaire.png', dpi=300, bbox_inches='tight')
plt.show()

# 6. Affichage des informations du modèle
print("\n" + "="*50)
print("📊 INFORMATIONS DU MODÈLE")
print("="*50)
print(f"Coefficient (pente): {model.coef_[0]:.2f}")
print(f"Interception: {model.intercept_:.2f}")
print(f"Équation: Salaire = {model.coef_[0]:.2f} × Années + {model.intercept_:.2f}")
print(f"Score R²: {r2_score:.3f}")
print("="*50)
print("✅ Modèle supervisé entraîné et sauvegardé !")

# 7. Test de prédiction pour quelques valeurs
print("\n🔍 EXEMPLES DE PRÉDICTIONS:")
print("-" * 40)
test_experiences = [1, 3, 5, 7, 10]
for exp in test_experiences:
    pred = model.predict([[exp]])[0]
    print(f"   {exp} an(s) d'expérience → Salaire prédit: ${pred:,.2f}")