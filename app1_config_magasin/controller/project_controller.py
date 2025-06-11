from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import Qt

class ProjectController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.create_btn.clicked.connect(self.handle_create_project)
        self.view.load_img_btn.clicked.connect(self.handle_load_image)

    def handle_create_project(self):
        name = self.view.project_name_input.text()
        author = self.view.author_input.text()
        address = self.view.address_input.text()

        self.model.set_project_info(name, author, address)
        self.model.set_grid_parameters(
        self.view.grid_size_input.value(),
        self.view.origin_x_input.value(),
        self.view.origin_y_input.value()
    )

    self.view.afficher_message("Projet enregistré avec succès.")

def handle_load_image(self):
    filename, _ = QFileDialog.getOpenFileName(self.view, "Charger une image", "", "Images (*.png *.jpg *.bmp)")
    if filename:
        self.model.set_image_path(filename)
        self.view.display_image_with_grid(
            filename,
            self.model.grid_size,
            self.model.grid_origin
        )