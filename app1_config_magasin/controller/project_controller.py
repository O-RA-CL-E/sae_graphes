from PyQt5.QtWidgets import QFileDialog, QPushButton
from model.project_model import ProjectModel
from view.project_view import ProjectView

class ProjectController:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.create_btn.clicked.connect(self.handle_create_project)
        self.view.load_img_btn.clicked.connect(self.handle_load_image)

        if not hasattr(self.view, 'save_btn'):
            self.view.save_btn = QPushButton("Sauvegarder projet")
            self.view.layout().addWidget(self.view.save_btn)
        self.view.save_btn.clicked.connect(self.handle_save_project)

        if not hasattr(self.view, 'auto_grid_btn'):
            self.view.auto_grid_btn = QPushButton("Quadrillage automatique")
            self.view.layout().addWidget(self.view.auto_grid_btn)
        self.view.auto_grid_btn.clicked.connect(self.handle_auto_grid)

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
            nb_cols = self.view.nb_cols_input.value()
            nb_rows = self.view.nb_rows_input.value()
            self.view.display_image_with_grid(filename, nb_cols, nb_rows)

    def handle_save_project(self):
        name = self.view.project_name_input.text()
        author = self.view.author_input.text()
        address = self.view.address_input.text()

        self.model.set_project_info(name, author, address)
        self.model.set_grid_parameters(
            self.view.grid_size_input.value(),
            self.view.origin_x_input.value(),
            self.view.origin_y_input.value()
        )

        self.model.save_to_file()
        self.view.afficher_message("Projet sauvegardé dans projets/projet.json")

    def handle_auto_grid(self):
        if not self.model.image_path:
            self.view.afficher_message("Veuillez charger une image d'abord.")
            return
        optimal_cols, optimal_rows = self.model.estimate_grid_from_image()
        self.view.nb_cols_input.setValue(optimal_cols)
        self.view.nb_rows_input.setValue(optimal_rows)
        self.view.display_image_with_grid(self.model.image_path, optimal_cols, optimal_rows)