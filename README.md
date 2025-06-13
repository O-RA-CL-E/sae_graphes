# 🛒 SAÉ - Graphes - Application IHM

### Participants :
- **LAFHAJ Ethan** — *O-RA-CL-E*
- **FLOC'H Maël** — *MaelFH*
- **JOURNEE Gabriel** — *BobTheBuilder*
- **QUILLOT Alexis** — *Haruko*

---

## 🎯 Objectif du projet

> Concevoir une application permettant de modéliser un magasin et d'optimiser le cheminement pour collecter les produits d'une liste de courses.  
L'application fonctionne en deux étapes :
- **App 1 (Configuration magasin)** : définir la configuration complète du magasin, quadrillage, position des produits, sauvegarde des projets.
- **App 2 (Calcul de parcours - à venir)** : calculer le chemin optimal pour récupérer les produits à partir d’une liste.

---

## 📂 Fonctionnalités de l'application de configuration (App1)

- Création de projet (nom, auteur, adresse, date…)
- Chargement d’un plan du magasin (image)
- Quadrillage automatique du plan
- Positionnement des produits via un quadrillage cliquable
- Chargement de la liste des produits depuis `PRODUITS/produits.txt`  
- Sauvegarde et chargement de projets (fichiers `.json`)
- Suppression de projets
- Sauvegarde automatique après chaque ajout de produit
- Sécurité par mot de passe lors du démarrage
- Interface moderne, épurée et stylisée

---

## 📦 Structure du dépôt

```bash
sae_graphes/
│
├── app1_config_magasin/
│   ├── main_app1.py
│   ├── model/project_model.py
│   ├── view/project_view.py
│   └── controller/project_controller.py
│
├── data/PRODUITS/produits.txt
├── projets/   # dossiers de sauvegarde
├── documentation/ (cahier des charges)
├── README.md
├── PLANNING.md
├── requirements.txt
└── .gitignore
