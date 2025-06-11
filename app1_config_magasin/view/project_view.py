from PyQt5.QtWidgets import (
QWidget, QLabel, QPushButton, QLineEdit, QFileDialog,
QVBoxLayout, QHBoxLayout, QSpinBox, QGridLayout, QMessageBox
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QFont
from PyQt5.QtCore import Qt

class ProjectView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration du magasin")

    # Champs texte
        self.project_name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.address_input = QLineEdit()

    # Boutons
        self.create_btn = QPushButton("Créer projet")
        self.load_img_btn = QPushButton("Charger plan")

    # Zone d'image
        self.image_label = QLabel("Aucune image")

    # Paramètres grille
        self.grid_size_input = QSpinBox()
        self.grid_size_input.setValue(50)

        self.origin_x_input = QSpinBox()
        self.origin_y_input = QSpinBox()

        self.nb_cols_input = QSpinBox()
        self.nb_cols_input.setMinimum(1)
        self.nb_cols_input.setMaximum(100)
        self.nb_cols_input.setValue(20)

        self.nb_rows_input = QSpinBox()
        self.nb_rows_input.setMinimum(1)
        self.nb_rows_input.setMaximum(100)
        self.nb_rows_input.setValue(15)

        self.init_ui()

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
        layout.addWidget(self.image_label)

        grid_settings = QHBoxLayout()
        grid_settings.addWidget(QLabel("Taille case :"))
        grid_settings.addWidget(self.grid_size_input)
        grid_settings.addWidget(QLabel("Origine X :"))
        grid_settings.addWidget(self.origin_x_input)
        grid_settings.addWidget(QLabel("Origine Y :"))
        grid_settings.addWidget(self.origin_y_input)
        grid_settings.addWidget(QLabel("Colonnes :"))
        grid_settings.addWidget(self.nb_cols_input)
        grid_settings.addWidget(QLabel("Lignes :"))
        grid_settings.addWidget(self.nb_rows_input)
        layout.addLayout(grid_settings)

        self.setLayout(layout)

    def afficher_message(self, texte):
        QMessageBox.information(self, "Information", texte)

    def display_image_with_grid(self, path, nb_cols=20, nb_rows=15):
        max_width, max_height = 1000, 800
        original_pixmap = QPixmap(path)
        scaled_pixmap = original_pixmap.scaled(
        max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation
        )

        width = scaled_pixmap.width()
        height = scaled_pixmap.height()

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

        for row in range(nb_rows):
            for col in range(nb_cols):
                label = chr(65 + col) + str(row + 1)
                x = col * grid_width + 4
                y = row * grid_height + 12
                painter.drawText(x, y, label)

        painter.end()
        self.image_label.setPixmap(scaled_pixmap)
        self.image_label.setScaledContents(True)
