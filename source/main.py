from app.store import Magasin

# Initialisation
magasin = Magasin("MonSupermarche")
magasin.charger_produits("data/products.json")

# Test
print("Produits chargés :", magasin.produits)
