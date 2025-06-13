import os, json, shutil
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
        self.view.auto_grid_btn.clicked.connect(self.handle_auto_grid)
        self.view.save_btn.clicked.connect(self.handle_save_project)
        self.view.load_project_btn.clicked.connect(self.handle_load_project)
        self.view.delete_btn.clicked.connect(self.handle_delete_project)
        self.view.parent_controller = self

        self.project_initialized = False

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

        if not self.project_initialized:
            self.view.afficher_message("Projet initialisé avec succès.")
            self.project_initialized = True

        self.auto_save_project()

    def handle_load_image(self):
        filename, _ = QFileDialog.getOpenFileName(self.view, "Charger une image", "", "Images (*.png *.jpg *.bmp)")
        if filename:
            self.model.set_image_path(filename)
            self.redraw_grid()

    def handle_auto_grid(self):
        if not self.model.image_path:
            self.view.afficher_message("Veuillez charger une image d'abord.")
            return

        image = QImage(self.model.image_path)
        width, height = image.width(), image.height()
        block_size = 20
        blocks_x = width // block_size
        blocks_y = height // block_size
        bright_blocks = 0
        total_blocks = blocks_x * blocks_y

        for bx in range(blocks_x):
            for by in range(blocks_y):
                sum_luminance = 0
                for dx in range(block_size):
                    for dy in range(block_size):
                        x = bx * block_size + dx
                        y = by * block_size + dy
                        if x < width and y < height:
                            pixel = image.pixel(x, y)
                            r = (pixel >> 16) & 0xFF
                            g = (pixel >> 8) & 0xFF
                            b = pixel & 0xFF
                            luminance = (r + g + b) / 3
                            sum_luminance += luminance

                avg_luminance = sum_luminance / (block_size * block_size)
                if avg_luminance > 220:
                    bright_blocks += 1

        white_ratio = bright_blocks / total_blocks
        optimal_cols = max(5, int(width / (30 + white_ratio * 70)))
        optimal_rows = max(5, int(height / (30 + white_ratio * 70)))

        self.view.nb_cols_input.setValue(optimal_cols)
        self.view.nb_rows_input.setValue(optimal_rows)
        self.redraw_grid()
        self.auto_save_project()

    def handle_place_product(self, col, row):
        label = self.view.product_selector.currentText().strip()
        self.model.add_product(label, col, row)
        self.redraw_grid()
        self.auto_save_project()

    def redraw_grid(self):
        if not self.model.image_path:
            return

        nb_cols = self.view.nb_cols_input.value()
        nb_rows = self.view.nb_rows_input.value()

        original_pixmap = QPixmap(self.model.image_path)
        scaled_pixmap = original_pixmap.scaled(1000, 800, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        width, height = scaled_pixmap.width(), scaled_pixmap.height()
        grid_width = width // nb_cols
        grid_height = height // nb_rows

        painter = QPainter(scaled_pixmap)
        pen = QPen(Qt.red, 1)
        painter.setPen(pen)
        painter.setFont(QFont("", 8))

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

    def handle_save_project(self):
        self.auto_save_project()
        self.view.afficher_message("Projet sauvegardé avec succès.")

    def auto_save_project(self):
        name = self.model.project_name
        if not name:
            return

        project_dir = os.path.join("projets", name)
        os.makedirs(project_dir, exist_ok=True)

        if self.model.image_path:
            image_filename = os.path.basename(self.model.image_path)
            dest_path = os.path.join(project_dir, image_filename)
            if not os.path.exists(dest_path):
                shutil.copy(self.model.image_path, dest_path)
            relative_image_path = os.path.join(name, image_filename)
        else:
            relative_image_path = ""

        project_file = os.path.join(project_dir, f"{name}.json")

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

    def handle_load_project(self):
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
        self.redraw_grid()
        self.view.afficher_message("Projet chargé avec succès.")

    def handle_delete_project(self):
        directory = QFileDialog.getExistingDirectory(self.view, "Sélectionner le dossier à supprimer", "projets/")
        if not directory:
            return
        confirmation = QMessageBox.question(self.view, "Supprimer ?", f"Supprimer le projet '{directory}' ?", QMessageBox.Yes | QMessageBox.No)
        if confirmation == QMessageBox.Yes:
            shutil.rmtree(directory)
            self.view.afficher_message("Projet supprimé.")