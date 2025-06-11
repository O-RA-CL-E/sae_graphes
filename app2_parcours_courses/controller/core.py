from model.magasin import Magasin
from view.interface import Interface

class Controller:
    def __init__(self):
        self.modele = Magasin()
        self.vue = Interface(self)
    
    def demarrer(self):
        self.vue.afficher_menu_principal()
    
    def charger_projet(self, chemin):
        return self.modele.charger_projet(chemin)
    
    def generer_liste(self):
        return self.modele.generer_liste_aleatoire()
