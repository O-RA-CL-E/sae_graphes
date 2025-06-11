import json

class ProjectModel:
    def __init__(self):
        self.project_name = ""
        self.author = ""
        self.address = ""
        self.creation_date = ""
        self.image_path = ""
        self.grid_size = 50
        self.grid_origin = (0, 0)
        self.products = []
        self.project_file = None

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
        self.products.append({"label": label, "col": col, "row": row})

    def get_products(self):
        return self.products
