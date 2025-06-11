import json
import random
from PyQt5.QtWidgets import QFileDialog
from view.fenetre_app2 import FenetreApp2

class ControllerApp2:
    def __init__(self):
        self.fenetre = FenetreApp2()
        self.produits_disponibles = []
        self.grille_info = {}

        self.fenetre.btn_charger.clicked.connect(self.charger_projet)
        self.fenetre.btn_generer.clicked.connect(self.generer_liste_courses)

    def run(self):
        self.fenetre.show()

    def charger_projet(self):
        chemin, _ = QFileDialog.getOpenFileName(
            self.fenetre, "Ouvrir un projet", "projets/", "Fichiers JSON (*.json)")
        if chemin:
            with open(chemin, 'r') as f:
                data = json.load(f)
            self.grille_info = data['grille']
            self.produits_disponibles = data['produits']
            self.fenetre.afficher_plan(data['plan'])
            self.fenetre.afficher_produits(
                self.produits_disponibles, self.grille_info)

    def generer_liste_courses(self):
        nb = min(15, len(self.produits_disponibles))
        liste_courses = random.sample(self.produits_disponibles, nb)
        self.fenetre.maj_liste_courses(liste_courses)
        self.fenetre.afficher_produits(
            liste_courses, self.grille_info, couleur='red')

