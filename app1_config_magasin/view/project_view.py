from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, 
    QHBoxLayout, QSpinBox, QGridLayout, QMessageBox, QComboBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class ProjectView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration du magasin")

        self.project_name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.address_input = QLineEdit()

        self.create_btn = QPushButton("Créer projet")
        self.load_img_btn = QPushButton("Charger plan")
        self.save_btn = QPushButton("Sauvegarder projet")
        self.load_project_btn = QPushButton("Charger projet")
        self.auto_grid_btn = QPushButton("Quadrillage automatique")
        self.delete_btn = QPushButton("Supprimer projet")

        self.image_label = QLabel("Aucune image")

        self.grid_size_input = QSpinBox(); self.grid_size_input.setValue(50)
        self.origin_x_input = QSpinBox(); self.origin_y_input = QSpinBox()
        self.nb_cols_input = QSpinBox(); self.nb_cols_input.setRange(1,100); self.nb_cols_input.setValue(20)
        self.nb_rows_input = QSpinBox(); self.nb_rows_input.setRange(1,100); self.nb_rows_input.setValue(15)

        self.product_selector = QComboBox()
        self.load_products_from_file("PRODUITS/produits")

        self.parent_controller = None
        self.image_label.mousePressEvent = self.handle_click_on_image
        self.init_ui()

    def load_products_from_file(self, filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("["):
                        continue
                    self.product_selector.addItem(line)
        except FileNotFoundError:
            QMessageBox.critical(self, "Erreur", f"Fichier produits introuvable : {filepath}")

    def init_ui(self):
        layout = QVBoxLayout()
        form_layout = QGridLayout()
        form_layout.addWidget(QLabel("Nom projet :"), 0, 0)
        form_layout.addWidget(self.project_name_input, 0, 1)
        form_layout.addWidget(QLabel("Auteur :"), 1, 0)
        form_layout.addWidget(self.author_input, 1, 1)
        form_layout.addWidget(QLabel("Adresse :"), 2, 0)
        form_layout.addWidget(self.address_input, 2, 1)
        layout.addLayout(form_layout)

        layout.addWidget(self.create_btn)
        layout.addWidget(self.load_img_btn)
        layout.addWidget(self.auto_grid_btn)
        layout.addWidget(self.save_btn)
        layout.addWidget(self.load_project_btn)
        layout.addWidget(self.delete_btn)
        layout.addWidget(self.image_label)

        grid_settings = QHBoxLayout()
        grid_settings.addWidget(QLabel("Taille case :")); grid_settings.addWidget(self.grid_size_input)
        grid_settings.addWidget(QLabel("Origine X :")); grid_settings.addWidget(self.origin_x_input)
        grid_settings.addWidget(QLabel("Origine Y :")); grid_settings.addWidget(self.origin_y_input)
        grid_settings.addWidget(QLabel("Colonnes :")); grid_settings.addWidget(self.nb_cols_input)
        grid_settings.addWidget(QLabel("Lignes :")); grid_settings.addWidget(self.nb_rows_input)
        layout.addLayout(grid_settings)

        layout.addWidget(QLabel("Produit à placer :"))
        layout.addWidget(self.product_selector)
        self.setLayout(layout)

    def afficher_message(self, texte):
        QMessageBox.information(self, "Information", texte)

    def handle_click_on_image(self, event):
        if not self.image_label.pixmap():
            return

        pos = event.pos()
        label_width = self.image_label.width()
        label_height = self.image_label.height()

        pixmap = self.image_label.pixmap()
        pixmap_width = pixmap.width()
        pixmap_height = pixmap.height()

        scale = min(label_width / pixmap_width, label_height / pixmap_height)
        displayed_width = pixmap_width * scale
        displayed_height = pixmap_height * scale
        margin_x = (label_width - displayed_width) / 2
        margin_y = (label_height - displayed_height) / 2

        x = (pos.x() - margin_x) / scale
        y = (pos.y() - margin_y) / scale

        if not (0 <= x < pixmap_width and 0 <= y < pixmap_height):
            return

        nb_cols = self.nb_cols_input.value()
        nb_rows = self.nb_rows_input.value()
        grid_w = pixmap_width / nb_cols
        grid_h = pixmap_height / nb_rows

        col = min(int(x / grid_w), nb_cols - 1)
        row = min(int(y / grid_h), nb_rows - 1)

        if self.parent_controller:
            self.parent_controller.handle_place_product(col, row)
