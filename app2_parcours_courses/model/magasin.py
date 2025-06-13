import json

class Magasin:
    def __init__(self, json_path):
        with open(json_path, "r") as f:
            data = json.load(f)
        self.nom = data.get("project_name", "")
        self.auteur = data.get("author", "")
        self.adresse = data.get("address", "")
        self.image_path = data.get("image_path", "")
        self.grid_size = data.get("grid_size", 50)
        self.grid_origin = data.get("grid_origin", [0, 0])
        self.products = data.get("products", [])
        self.nb_cols = data.get("nb_cols", 20)
        self.nb_rows = data.get("nb_rows", 15)