import json
import os
import shutil
from datetime import datetime
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont, QImage
from PyQt5.QtCore import Qt

class ProjectController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.create_btn.clicked.connect(self.handle_create_project)
        self.view.load_img_btn.clicked.connect(self.handle_load_image)
        self.view.save_btn.clicked.connect(self.handle_save_project)
        self.view.load_project_btn.clicked.connect(self.handle_load_project)
        self.view.auto_grid_btn.clicked.connect(self.handle_auto_grid)
        self.view.delete_btn.clicked.connect(self.handle_delete_project)
        self.view.parent_controller = self

    def handle_create_project(self):
        name = self.view.project_name_input.text()
        author = self.view.author_input.text()
        address = self.view.address_input.text()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.model.set_project_info(name, author, address)
        self.model.creation_date = date
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
            self.redraw_grid()

    def handle_save_project(self):
        self.handle_create_project()
        name = self.view.project_name_input.text()
        project_dir = os.path.join("projets", name)
        os.makedirs(project_dir, exist_ok=True)

        if self.model.image_path:
            image_filename = os.path.basename(self.model.image_path)
            destination_path = os.path.join(project_dir, image_filename)
            if not os.path.exists(destination_path):
                shutil.copy(self.model.image_path, destination_path)
            relative_image_path = os.path.join(name, image_filename)
        else:
            relative_image_path = ""

        file_dialog = QFileDialog(self.view)
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setDefaultSuffix("json")
        file_dialog.setNameFilter("Fichiers projet (*.json)")
        file_dialog.setDirectory(project_dir)

        if file_dialog.exec_():
            project_file = file_dialog.selectedFiles()[0]
        else:
            return

        self.model.project_file = project_file
        data = {
            "project_name": self.model.project_name,
            "author": self.model.author,
            "address": self.model.address,
            "creation_date": self.model.creation_date,
            "image_path": relative_image_path,
            "grid_size": self.model.grid_size,
            "grid_origin": self.model.grid_origin,
            "nb_cols": self.view.nb_cols_input.value(),
            "nb_rows": self.view.nb_rows_input.value(),
            "products": self.model.get_products()
        }
        with open(project_file, "w") as f:
            json.dump(data, f, indent=4)
        self.view.afficher_message(f"Projet sauvegardé dans {project_file}")

    def handle_place_product(self, col, row):
        label = self.view.product_selector.currentText()
        self.model.add_product(label, col, row)
        self.redraw_grid()
        self.auto_save_project()

    def auto_save_project(self):
        if not self.model.project_file:
            return
        name = self.view.project_name_input.text()
        relative_image_path = self.model.image_path
        if os.path.isabs(self.model.image_path):
            relative_image_path = os.path.relpath(self.model.image_path, "projets")
        data = {
            "project_name": self.model.project_name,
            "author": self.model.author,
            "address": self.model.address,
            "creation_date": self.model.creation_date,
            "image_path": relative_image_path,
            "grid_size": self.model.grid_size,
            "grid_origin": self.model.grid_origin,
            "nb_cols": self.view.nb_cols_input.value(),
            "nb_rows": self.view.nb_rows_input.value(),
            "products": self.model.get_products()
        }
        with open(self.model.project_file, "w") as f:
            json.dump(data, f, indent=4)

    def handle_load_project(self):
        try:
            filename, _ = QFileDialog.getOpenFileName(self.view, "Charger un projet", "projets/", "Fichiers projet (*.json)")
            if not filename:
                return
            with open(filename, "r") as f:
                data = json.load(f)

            self.view.project_name_input.setText(data.get("project_name", ""))
            self.view.author_input.setText(data.get("author", ""))
            self.view.address_input.setText(data.get("address", ""))
            self.view.grid_size_input.setValue(data.get("grid_size", 50))
            origin_x, origin_y = data.get("grid_origin", [0, 0])
            self.view.origin_x_input.setValue(origin_x)
            self.view.origin_y_input.setValue(origin_y)
            self.view.nb_cols_input.setValue(data.get("nb_cols", 20))
            self.view.nb_rows_input.setValue(data.get("nb_rows", 15))

            image_path = data.get("image_path", "")
            full_image_path = os.path.join("projets", image_path)
            if os.path.exists(full_image_path):
                self.model.set_image_path(full_image_path)
            else:
                self.view.afficher_message("Image non trouvée : " + full_image_path)

            self.model.products = data.get("products", [])
            self.model.project_file = filename
            self.redraw_grid()
            self.view.afficher_message("Projet chargé avec succès.")
        except Exception as e:
            self.view.afficher_message(f"Erreur lors du chargement : {e}")

    def handle_auto_grid(self):
        if not self.model.image_path:
            self.view.afficher_message("Veuillez charger une image d'abord.")
            return

        image = QImage(self.model.image_path)
        width, height = image.width(), image.height()

        optimal_cols = max(5, width // 50)
        optimal_rows = max(5, height // 50)

        self.view.nb_cols_input.setValue(optimal_cols)
        self.view.nb_rows_input.setValue(optimal_rows)
        self.redraw_grid()

    def redraw_grid(self):
        if not self.model.image_path:
            return
        nb_cols = self.view.nb_cols_input.value()
        nb_rows = self.view.nb_rows_input.value()
        max_width, max_height = 1000, 800
        original_pixmap = QPixmap(self.model.image_path)
        scaled_pixmap = original_pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        width, height = scaled_pixmap.width(), scaled_pixmap.height()
        grid_width = width // nb_cols
        grid_height = height // nb_rows

        painter = QPainter(scaled_pixmap)
        pen = QPen(Qt.red)
        pen.setWidth(1)
        painter.setPen(pen)
        font = QFont()
        font.setPointSize(8)
        painter.setFont(font)

        for x in range(0, width, grid_width):
            painter.drawLine(x, 0, x, height)
        for y in range(0, height, grid_height):
            painter.drawLine(0, y, width, y)

        for product in self.model.get_products():
            px = product["col"] * grid_width
            py = product["row"] * grid_height
            painter.setPen(QPen(Qt.blue, 2))
            painter.drawRect(px, py, grid_width, grid_height)
            painter.drawText(px + 5, py + 15, product["label"])

        painter.end()
        self.view.image_label.setPixmap(scaled_pixmap)
        self.view.image_label.setScaledContents(True)

    def handle_delete_project(self):
        directory = QFileDialog.getExistingDirectory(self.view, "Sélectionner le dossier du projet à supprimer", "projets/")
        if not directory:
            return
        confirmation = QMessageBox.question(self.view, "Confirmation", f"Supprimer le projet '{directory}' ?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            shutil.rmtree(directory)
            self.view.afficher_message("Projet supprimé avec succès.")