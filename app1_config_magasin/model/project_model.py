import json, os
from PyQt5.QtGui import QImage

class ProjectModel:
    def __init__(self):
        self.project_name = ""
        self.author = ""
        self.address = ""
        self.image_path = ""
        self.grid_size = 50
        self.grid_origin = (0, 0)
        self.products = []  # liste des produits placés

    def set_project_info(self, name, author, address):
        self.project_name = name
        self.author = author
        self.address = address

    def set_image_path(self, path):
        self.image_path = path

    def set_grid_parameters(self, size, origin_x, origin_y):
        self.grid_size = size
        self.grid_origin = (origin_x, origin_y)

    def add_product(self, label, col, row):
        self.products.append({
            "label": label,
            "col": col,
            "row": row
        })

    def get_products(self):
        return self.products

    def save_to_file(self, filepath="projets/projet.json"):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        data = {
            "project_name": self.project_name,
            "author": self.author,
            "address": self.address,
            "image_path": self.image_path,
            "grid_size": self.grid_size,
            "grid_origin": self.grid_origin,
            "products": self.get_products()
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def estimate_grid_from_image(self):
        if not self.image_path:
            return 20, 15
        image = QImage(self.image_path)
        width, height = image.width(), image.height()
        optimal_cols = max(1, width // 50)
        optimal_rows = max(1, height // 50)
        return optimal_cols, optimal_rows