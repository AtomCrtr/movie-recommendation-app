# 🎥 **CinéMatch - Movie Recommendation App**

## 🌟 **Description**
**CinéMatch** est un moteur de recommandation de films conçu pour un cinéma local de la Creuse. Ce projet utilise des bases de données, des algorithmes de machine learning et une interface interactive pour offrir des recommandations personnalisées et des insights pertinents pour les cinémas.

**💡 Objectifs :**
- Proposer des recommandations adaptées aux goûts des spectateurs.
- Optimiser la gestion des franchises et des films à l’affiche.

---

## 📊 **Plan de réalisation**

### Étape 1 : Étude de marché
- Analyse des tendances locales dans la Creuse :
  - Population cible : 45-75 ans.
  - Genres préférés : Films français, Arts et essais, Films US.
- Analyse des données nationales via INSEE, CNC, et Google.

### Étape 2 : Exploration et nettoyage des données
- **Sources :** IMDb et TMDB.
- Sélection et tri :
  - Conservation des films français uniquement.
  - Exclusion des doublons et films non pertinents (adultes, sans date de sortie, etc.).
- Génération d'une table unique pour l'analyse.

### Étape 3 : Machine learning et recommandations
- Nettoyage des textes (stopwords, stemmatisation).
- Vectorisation avec **TF-IDF**.
- Modèle de similarité avec **Nearest Neighbors (cosinus)** pour proposer des recommandations précises.

### Étape 4 : Interface et présentation
- Développement avec **Streamlit** :
  - Page 1 : Recommandations personnalisées.
  - Page 2 : Films à l'affiche dans la Creuse (scrapés via Allociné).
  - Page 3 : Quiz interactif pour des suggestions sur mesure.

---

## 🛠️ **Technologies et outils**

### **Analyse de données :**
- **Python :** Pandas, DuckDB, Regex, NLTK.
- **Jupyter Notebook / Google Colab.**
- **Power BI :** Visualisation des KPI.

### **Développement web :**
- **Streamlit :** Création de l’application.

### **Collaboration :**
- **Slack, Trello** pour la gestion de projet.

---

## 🚀 **Fonctionnalités**

### 🎯 Recommandations personnalisées
- Suggestions basées sur le genre, la note et les années.
- Algorithmes de machine learning pour des résultats précis.

### 🕒 Films à l'affiche
- Affichage des films actuellement diffusés dans les cinémas locaux.
- Web scraping automatisé (Allociné).

### 📋 Quiz interactif
- Aide les spectateurs à trouver des films correspondant à leurs préférences.

---

## 📈 **Améliorations prévues**
- Optimisation des algorithmes de machine learning.
- Ajout de fonctionnalités : favoris, listes d’envies, notifications.
- Intégration de **Power BI** dans Streamlit pour des graphiques interactifs.

---

## 🖥️ **Lancement du projet**

### Prérequis
1. **Python 3.8+** installé.
2. Installer les dépendances avec :
   ```bash
   pip install -r requirements.txt
   ```

### Exécution
1. Clonez le dépôt GitHub :
   ```bash
   git clone https://github.com/ton_nom_utilisateur/movie-recommendation-app.git
   cd movie-recommendation-app
   ```
2. Lancez l'application :
   ```bash
   streamlit run Projet\ 2/Site/site.py
   ```
3. Ouvrez le lien généré dans votre navigateur.

---

## 📋 **Livrables**
- **Google Slides :** [Présentation ici](https://docs.google.com/presentation/d/1K1pr7uvhdbb3xMq3mcDfZKsLTJVWkJJGXbcdvbNOBT8/edit?usp=sharing)
- **Dépôt Streamlit :** [Code source ici](Projet%202/Site/site.py).
- **Google Collab :** [Code ici](https://colab.research.google.com/drive/1duQXYu8l2x3VLOw4mfs9PNPvnlwJ3b_K?usp=sharing)

---

## 🤝 **Contributeurs**
- **Équipe CinéMatch (Gadjos).**
