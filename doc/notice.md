# 📖 Notice d'utilisation - SAÉ IHM - Configuration magasin

## ⚙️ Pré-requis

- Python 3.10+
- Modules requis (voir `requirements.txt`)

## 📦 Installation

1️⃣ Cloner le projet :

```bash
git clone https://github.com/O-RA-CL-E/sae_graphes.git
```

## 🚀 Lancement de l’application

1. Ouvrez un terminal.
2. Activez votre environnement virtuel (si besoin) :
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```
3. Lancez l’application avec :
```bash
python app1_config_magasin/main_app1.py
```

## 🔑 Connexion

- Lors du lancement, entrez le mot de passe requis :  
**`root`**

## 🛠 Fonctionnalités principales

### 1️⃣ **Créer un projet**
- Remplissez :
  - **Nom du projet**
  - **Auteur**
  - **Adresse**
- Cliquez sur **"Créer projet"**.

### 2️⃣ **Charger le plan du magasin**
- Cliquez sur **"Charger plan"**.
- Sélectionnez l’image du plan de votre magasin (formats supportés : PNG, JPG, BMP).

### 3️⃣ **Quadrillage automatique (facultatif)**
- Cliquez sur **"Quadrillage automatique"** pour générer un quadrillage optimal selon le plan chargé.
- Vous pouvez ajuster manuellement le nombre de **colonnes** et de **lignes**.

### 4️⃣ **Placer des produits**
- En bas de la fenêtre, sélectionnez un produit dans la liste.
- Cliquez directement sur la case du quadrillage où vous souhaitez positionner le produit.

> 🔎 Vous pouvez rechercher un produit en commençant à taper son nom.

> 🧠 **Protection intégrée** : il est impossible de placer plusieurs fois un produit sur la même case.

### 5️⃣ **Sauvegarder le projet**
- Cliquez sur **"Sauvegarder projet"**.
- Donnez un nom au fichier `.json` et confirmez.
- ✅ **Sauvegarde automatique** à chaque modification de placement.

### 6️⃣ **Charger un projet existant**
- Cliquez sur **"Charger projet"**.
- Sélectionnez un fichier projet existant.

### 7️⃣ **Supprimer un projet**
- Cliquez sur **"Supprimer projet"** pour effacer un projet existant (dossier complet supprimé).

## 📂 Structure de sauvegarde

Chaque projet contient :
- Fichier `.json` avec :
  - Informations du projet
  - Paramètres du quadrillage
  - Positions des produits
- Plan du magasin (copie de l’image source)

✅ **Application stable, ergonomique, sécurisée et prête pour l’exploitation**.

## 🚀 Lancement de l’application 2

1. Lancez l’application avec :
```bash
python app2_parcours_courses/main.py
```

## 🔑 Connexion

- Lors du lancement, entrez le mot de passe requis :  
**`root`**

## 🛠 Fonctionnalités principales

### 1️⃣ **Charger le magasin**
- Cliquez sur **"Charger un magasin"**.
- Sélectionnez un fichier projet existant.

### 2️⃣ **mettre des produits dans la liste de courses**
- double cliquer sur les articles qui sont en dessous du plan du magasin

### 3️⃣ **Générer une liste de courses aléatoire (facultatif)**
- cliquez sur le bouton **"Générer une liste de courses aléatoire"**

### 4️⃣ **tracer le chemin le plus court**
- pour tracer le chemin le plus court, cliquez sur le bouton **"Tracer le chemin le plus court"**

### 5️⃣ **Suppression de produit dans la liste de cours**
- pour supprimer un produit de la liste de cours, il faut double-cliquer sur le produit que vous voulez enlever dans la liste de courses
