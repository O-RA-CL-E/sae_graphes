import json
import random

class Magasin:
    def __init__(self):
        self.produits = []
        self.plan = ""
    
    def charger_projet(self, chemin_projet):
        try:
            with open(f"{chemin_projet}/produits.json") as f:
                self.produits = json.load(f)
            self.plan = f"{chemin_projet}/plan.png"
            return True
        except:
            return False
    
    def generer_liste_aleatoire(self, n=5):
        return random.sample(self.produits, n)
