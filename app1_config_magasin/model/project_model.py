import json
import os
from PyQt5.QtGui import QImage

class ProjectModel:
    def __init__(self):
        self.project_name = ""
        self.author = ""
        self.address = ""
        self.image_path = ""
        self.grid_size = 50
        self.grid_origin = (0, 0)

    def set_project_info(self, name, author, address):
        self.project_name = name
        self.author = author
        self.address = address

    def set_image_path(self, path):
        self.image_path = path

    def set_grid_parameters(self, size, origin_x, origin_y):
        self.grid_size = size
        self.grid_origin = (origin_x, origin_y)

    def save_to_file(self, filepath="projets/projet.json"):
        data = {
            "project_name": self.project_name,
            "author": self.author,
            "address": self.address,
            "image_path": self.image_path,
            "grid_size": self.grid_size,
            "grid_origin": self.grid_origin
        }
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    def estimate_grid_from_image(self):
        if not self.image_path:
            return 20, 15  # valeur par défaut
        img = QImage(self.image_path)
        width = img.width()
        height = img.height()

        best_cols = 20
        best_rows = 15
        best_score = 0

        for cols in range(10, 41, 5):
            for rows in range(10, 31, 5):
                grid_w = width // cols
                grid_h = height // rows
                score = 0
                for y in range(0, height, grid_h):
                    for x in range(0, width, grid_w):
                        count = 0
                        for i in range(0, grid_w, max(1, grid_w//5)):
                            for j in range(0, grid_h, max(1, grid_h//5)):
                                if x + i < width and y + j < height:
                                    pixel = img.pixelColor(x + i, y + j)
                                    brightness = (pixel.red() + pixel.green() + pixel.blue()) / 3
                                    if brightness > 220:
                                        count += 1
                        score += count
                if score > best_score:
                    best_score = score
                    best_cols = cols
                    best_rows = rows

        return best_cols, best_rows