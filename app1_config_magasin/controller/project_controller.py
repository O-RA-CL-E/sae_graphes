from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt
import json, os

class ProjectController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.create_btn.clicked.connect(self.handle_create_project)
        self.view.load_img_btn.clicked.connect(self.handle_load_image)
        self.view.save_btn.clicked.connect(self.handle_save_project)
        self.view.load_project_btn.clicked.connect(self.handle_load_project)
        self.view.auto_grid_btn.clicked.connect(self.handle_auto_grid)
        self.view.parent_controller = self

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
        self.handle_create_project()
        self.model.save_to_file()
        self.view.afficher_message("Projet sauvegardé dans projets/projet.json")

    def handle_load_project(self):
        try:
            with open("projets/projet.json", "r") as f:
                data = json.load(f)
            self.view.project_name_input.setText(data.get("project_name", ""))
            self.view.author_input.setText(data.get("author", ""))
            self.view.address_input.setText(data.get("address", ""))
            self.view.grid_size_input.setValue(data.get("grid_size", 50))
            origin_x, origin_y = data.get("grid_origin", [0, 0])
            self.view.origin_x_input.setValue(origin_x)
            self.view.origin_y_input.setValue(origin_y)
            image_path = data.get("image_path", "")
            if os.path.exists(image_path):
                self.model.set_image_path(image_path)
                nb_cols = self.view.nb_cols_input.value()
                nb_rows = self.view.nb_rows_input.value()
                self.view.display_image_with_grid(image_path, nb_cols, nb_rows)
            else:
                self.view.afficher_message("Image non trouvée : " + image_path)
            self.view.afficher_message("Projet chargé avec succès.")
        except Exception as e:
            self.view.afficher_message(f"Erreur lors du chargement : {e}")

    def handle_auto_grid(self):
        if not self.model.image_path:
            self.view.afficher_message("Veuillez charger une image d'abord.")
            return
        optimal_cols, optimal_rows = self.model.estimate_grid_from_image()
        self.view.nb_cols_input.setValue(optimal_cols)
        self.view.nb_rows_input.setValue(optimal_rows)
        self.view.display_image_with_grid(self.model.image_path, optimal_cols, optimal_rows)

    def handle_place_product(self, col, row):
        label = self.view.product_selector.currentText()
        nb_cols = self.view.nb_cols_input.value()
        nb_rows = self.view.nb_rows_input.value()
        pixmap = QPixmap(self.model.image_path)
        pixmap = pixmap.scaled(1000, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        width = pixmap.width()
        height = pixmap.height()
        grid_w = width // nb_cols
        grid_h = height // nb_rows
        x = col * grid_w
        y = row * grid_h
        painter = QPainter(pixmap)
        pen = QPen(Qt.red); pen.setWidth(2); painter.setPen(pen)
        font = QFont(); font.setPointSize(10); painter.setFont(font)
        painter.drawRect(x, y, grid_w, grid_h)
        painter.drawText(x + 4, y + 16, label)
        painter.end()
        self.view.image_label.setPixmap(pixmap)
        self.model.add_product(label, col, row)
