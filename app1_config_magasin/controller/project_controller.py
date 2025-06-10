from PyQt5.QtWidgets import (
QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout,
QHBoxLayout, QSpinBox, QGridLayout
)
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt

class ProjectView(QWidget):
    def init(self):
        super().init()
        self.setWindowTitle("Configuration du magasin")

        self.project_name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.address_input = QLineEdit()

        self.create_btn = QPushButton("Creation projet")
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

def detect_empty_cells(self, path, grid_size):
    img = QImage(path)
    width = img.width()
    height = img.height()
    empty_cells = []

    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            brightness_values = []
            for i in range(grid_size):
                for j in range(grid_size):
                    if x + i < width and y + j < height:
                        pixel = img.pixel(x + i, y + j)
                        r = (pixel >> 16) & 0xFF
                        g = (pixel >> 8) & 0xFF
                        b = pixel & 0xFF
                        brightness = (r + g + b) / 3
                        brightness_values.append(brightness)
            avg_brightness = sum(brightness_values) / len(brightness_values)
            if avg_brightness > 220:
                empty_cells.append((x, y))
    return empty_cells

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

    empty_cells = self.detect_empty_cells(path, grid_size)
    for x, y in empty_cells:
        painter.fillRect(x, y, grid_size, grid_size, Qt.green)

    painter.end()
    self.image_label.setPixmap(pixmap)
    self.image_label.setScaledContents(True)
