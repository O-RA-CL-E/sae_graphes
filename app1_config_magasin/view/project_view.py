from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout, QHBoxLayout, QSpinBox, QGridLayout, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt

class ProjectView(QWidget):
    def init(self):
        super().init()
        self.setWindowTitle("Configuration du magasin")

        self.project_name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.address_input = QLineEdit()

        self.create_btn = QPushButton("Créer projet")
        self.load_img_btn = QPushButton("Charger plan")
        self.image_label = QLabel("Aucune image")

        self.grid_size_input = QSpinBox()
        self.grid_size_input.setValue(50)

        self.origin_x_input = QSpinBox()
        self.origin_y_input = QSpinBox()

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
    layout.addLayout(grid_settings)

    self.setLayout(layout)

def afficher_message(self, texte):
    QMessageBox.information(self, "Information", texte)

def display_image_with_grid(self, path, grid_size, origin):
    pixmap = QPixmap(path)
    painter = QPainter(pixmap)
    pen = QPen(Qt.red)
    pen.setWidth(1)
    painter.setPen(pen)

    width = pixmap.width()
    height = pixmap.height()
    ox, oy = origin

    for x in range(ox, width, grid_size):
        painter.drawLine(x, 0, x, height)
    for y in range(oy, height, grid_size):
        painter.drawLine(0, y, width, y)

    painter.end()
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True) 
