# 🛒 SAÉ - Graphes - Application IHM

## 🎓 Projet universitaire (BUT1 - SAÉ 2.02)

> Projet de fin de semestre : création d'une double application permettant de configurer un magasin (App1) et d'optimiser un parcours de courses (App2).

---

## 🎯 Objectif du projet

> Concevoir une application permettant de modéliser un magasin et d'optimiser le cheminement pour collecter les produits d'une liste de courses.  
L'application fonctionne en deux étapes :
- 📐 App 1 (Configuration magasin) : définir la configuration complète du magasin, quadrillage, position des produits, sauvegarde des projets.
- 🧭 App 2 (Calcul de parcours) : calculer le chemin optimal pour récupérer les produits à partir d’une liste de courses.

---

## 🧰 Technologies utilisées

- Python 3.10+
- PyQt5
- Architecture MVC (Model - View - Controller)
- Sauvegarde JSON

---

## 👥 Participants

- 👤 LAFHAJ Ethan — O-RA-CL-E
- 👤 FLOC'H Maël — MaelFH
- 👤 JOURNEE Gabriel — BobTheBuilder
- 👤 QUILLOT Alexis — Haruko

---

## ⚙️ Installation

1. Cloner le projet :
```bash
git clone https://github.com/O-RA-CL-E/sae_graphes.git
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
venv\Scripts\activate     # Windows
```

3. Installer les dépendances :
```bash
pip install PyQt5
```

---

## 🚀 Lancement des applications

### App 1 — Configuration magasin
```bash
python app1_config_magasin/main_app1.py
```
Mot de passe au démarrage : `root`

### App 2 — Parcours de courses
```bash
python app2_parcours_courses/main.py
```
Mot de passe au démarrage : `root`

---

## 🛠 Fonctionnalités principales

### 🧱 App 1 — Configuration du magasin

- Création d’un projet (nom, auteur, adresse)
- Chargement du plan du magasin (image PNG, JPG, BMP)
- Quadrillage automatique (nombre de colonnes/lignes ajustables)
- Affichage dynamique des cellules (A1, B2, etc.)
- Placement de produits via clic sur les cellules
- Sauvegarde automatique au format JSON
- Chargement et suppression de projets

### 🧭 App 2 — Parcours de courses

- Chargement d’un projet existant
- Ajout de produits à la liste de courses par double-clic
- Génération aléatoire d’une liste de courses
- Suppression de produits de la liste de courses
- Calcul et affichage du chemin optimal sur le plan du magasin

---

## 📁 Structure du dépôt

```
sae_graphes/
│
├── PLANS/plan.jpg
├── PRODUITS/produits.txt
├── PROJETS/
├── app1_config_magasin/
│   ├── main_app1.py
│   ├── model/
│       └── project_model.py
│   ├── view/
│       └── project_view.py
│   └── controller/
│       └── project_controller.py
│
├── app2_parcours_courses/
│   ├── main.py
│   ├── model/
│       └── magasin.py
│   ├── view/
│       └── main_view.py
│   └── controller/
│       └── MainController.py
│
├── doc/
|   ├── notice.md
|   └── planning.md
├── .gitignore
└── README.md
```

---

## 📦 Structure de sauvegarde

Chaque projet contient :
- Un fichier `.json` avec :
  - Informations du projet
  - Paramètres du quadrillage
  - Coordonnées des produits placés
- Une copie de l’image du plan du magasin

---

## ✅ Remarques

- Interface graphique simple, claire et fonctionnelle
- Protection par mot de passe au démarrage des 2 applications
- Sauvegarde automatique à chaque action

---
