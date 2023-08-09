import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns


# Extraction
data = pd.read_csv('data/Netflix_Userbase.csv')


# Afficher les premières lignes pour vérification
print(data.head())

# Transformation - Nettoyage des données
# Transformation - Nettoyage des données avec spécification du format de date
data['Join Date'] = pd.to_datetime(data['Join Date'], format='%d-%m-%y')
data['Last Payment Date'] = pd.to_datetime(data['Last Payment Date'], format='%d-%m-%y')

# Remplacer les valeurs manquantes par des valeurs appropriées
data['Age'].fillna(data['Age'].median(), inplace=True)

# Enlever les espaces en début et fin de chaîne dans les valeurs textuelles
data['Country'] = data['Country'].str.strip()

# Filtrer les valeurs fausses (âge négatif par exemple)
data = data[data['Age'] > 0]

# Enlever les colonnes non pertinentes
data.drop(['User ID', 'Last Payment Date'], axis=1, inplace=True)

# Chargement (dans cet exemple, nous allons afficher les données nettoyées)
print(data.head())

# Chargement - Stockage des données nettoyées dans un fichier CSV
data.to_csv('data/cleaned_data.csv', index=False)

# Stockage des Données Transformées
# Configuration de la connexion à la base de données MySQL
db_username = 'root'
db_password = 'kiki'
db_host = 'localhost'
db_name = 'netflix_data_db'

# Création d'un moteur de base de données
db_engine = create_engine(f'mysql://{db_username}:{db_password}@{db_host}/{db_name}')

# Stockage des données dans la base de données
data.to_sql('netflix_data', con=db_engine, if_exists='replace', index=False)

# Fermeture de la connexion
db_engine.dispose()

# Analyse exploratoire avec visualisations
plt.figure(figsize=(12, 6))

# Répartition des abonnements par pays et type d'abonnement
plt.subplot(1, 2, 1)
sns.countplot(data=data, x='Country', hue='Subscription Type')
plt.title('Répartition des abonnements par pays')
plt.xlabel('Pays')
plt.ylabel('Nombre d\'abonnements')
plt.xticks(rotation=45)
plt.legend(title='Type d\'abonnement')

# Répartition des âges par pays
plt.subplot(1, 2, 2)
sns.boxplot(data=data, x='Country', y='Age')
plt.title('Répartition des âges par pays')
plt.xlabel('Pays')
plt.ylabel('Âge')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()





