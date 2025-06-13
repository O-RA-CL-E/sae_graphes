from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QLineEdit, QFileDialog, QVBoxLayout,
    QHBoxLayout, QSpinBox, QGridLayout, QMessageBox, QComboBox, QScrollArea, QGroupBox, QFormLayout
)
from PyQt5.QtGui import QPixmap, QStandardItemModel, QStandardItem, QFont
from PyQt5.QtCore import Qt
import os

class ProjectView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuration du magasin")
        self.setStyleSheet("""
    QWidget { 
        font-family: 'Segoe UI'; 
        font-size: 12pt; 
        background-color: #1c1c28; 
        color: #E0E0E0;  
    }
    QGroupBox { 
        background-color: #29293d; 
        border: 1px solid #3c3c55; 
        border-radius: 12px; 
        padding: 15px; 
        margin-top: 10px;
    }
                           
        QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top center;
        padding: 0 10px;
        font-size: 13pt;
        font-weight: 600;
        color: #f0f0f0;
    }
    QPushButton { 
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #4a4a70, stop:1 #3b3b60);
        border: 1px solid #5a5a80; 
        border-radius: 10px; 
        padding: 10px 15px;
        color: #ffffff;
        font-weight: 500;
        transition: all 0.3s;
    }
    QPushButton:hover { 
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #606090, stop:1 #505080);
    }
    QLineEdit, QSpinBox, QComboBox { 
        background-color: #303048; 
        border: 1px solid #505070; 
        border-radius: 8px; 
        padding: 6px 10px; 
        color: #ffffff;
        selection-background-color: #606080;
        selection-color: #ffffff;
    }
    QLabel { 
        color: #f0f0f0; 
        background: transparent;
    }
    QFormLayout > QLabel { 
        color: #f0f0f0;
        background: transparent;
    }
""")

        self.project_name_input = QLineEdit()
        self.author_input = QLineEdit()
        self.address_input = QLineEdit()
        self.create_btn = QPushButton("Créer projet")
        self.load_img_btn = QPushButton("Charger plan")
        self.auto_grid_btn = QPushButton("Quadrillage automatique")
        self.save_btn = QPushButton("Sauvegarder projet")
        self.load_project_btn = QPushButton("Charger projet")
        self.delete_btn = QPushButton("Supprimer projet")
        self.image_label = QLabel()
        self.image_label.setScaledContents(True)
        self.image_label_scroll = QScrollArea()
        self.image_label_scroll.setWidgetResizable(True)
        self.image_label_scroll.setWidget(self.image_label)
        self.grid_size_input = QSpinBox(); self.grid_size_input.setValue(50)
        self.origin_x_input = QSpinBox(); self.origin_y_input = QSpinBox()
        self.nb_cols_input = QSpinBox(); self.nb_cols_input.setRange(1, 100); self.nb_cols_input.setValue(20)
        self.nb_rows_input = QSpinBox(); self.nb_rows_input.setRange(1, 100); self.nb_rows_input.setValue(15)
        self.product_selector = QComboBox()
        self.load_products_from_file("PRODUITS/produits")
        self.parent_controller = None
        self.image_label.mousePressEvent = self.handle_click_on_image
        self.init_ui()

    def load_products_from_file(self, filepath):
        try:
            model = QStandardItemModel()
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.rstrip('\n\r')
                    if not line: continue
                    if line.startswith("[") and line.endswith("]"):
                        category_item = QStandardItem(line)
                        font = QFont(); font.setBold(True); category_item.setFont(font)
                        category_item.setFlags(Qt.NoItemFlags)
                        model.appendRow(category_item)
                    else:
                        product_item = QStandardItem("  " + line)
                        model.appendRow(product_item)
            self.product_selector.setModel(model)
        except FileNotFoundError:
            QMessageBox.critical(self, "Erreur", f"Fichier produits introuvable : {filepath}")

    def init_ui(self):
        layout = QVBoxLayout()

        form_box = QGroupBox("Informations projet")
        form_layout = QFormLayout()
        form_layout.addRow("Nom projet :", self.project_name_input)
        form_layout.addRow("Auteur :", self.author_input)
        form_layout.addRow("Adresse :", self.address_input)
        form_box.setLayout(form_layout)
        layout.addWidget(form_box)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.load_img_btn)
        button_layout.addWidget(self.auto_grid_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.load_project_btn)
        button_layout.addWidget(self.delete_btn)
        layout.addLayout(button_layout)

        grid_box = QGroupBox("Paramètres quadrillage")
        grid_layout = QGridLayout()
        grid_layout.addWidget(QLabel("Taille case :"), 0, 0)
        grid_layout.addWidget(self.grid_size_input, 0, 1)
        grid_layout.addWidget(QLabel("Origine X :"), 0, 2)
        grid_layout.addWidget(self.origin_x_input, 0, 3)
        grid_layout.addWidget(QLabel("Origine Y :"), 0, 4)
        grid_layout.addWidget(self.origin_y_input, 0, 5)
        grid_layout.addWidget(QLabel("Colonnes :"), 1, 0)
        grid_layout.addWidget(self.nb_cols_input, 1, 1)
        grid_layout.addWidget(QLabel("Lignes :"), 1, 2)
        grid_layout.addWidget(self.nb_rows_input, 1, 3)
        grid_box.setLayout(grid_layout)
        layout.addWidget(grid_box)

        layout.addWidget(self.image_label_scroll)

        product_box = QGroupBox("Placer un produit")
        product_layout = QVBoxLayout()
        product_layout.addWidget(self.product_selector)
        product_box.setLayout(product_layout)
        layout.addWidget(product_box)

        self.setLayout(layout)

    def afficher_message(self, texte):
        QMessageBox.information(self, "Information", texte)

    def handle_click_on_image(self, event):
        if not self.image_label.pixmap(): return
        x = event.pos().x() * self.image_label.pixmap().width() / self.image_label.width()
        y = event.pos().y() * self.image_label.pixmap().height() / self.image_label.height()
        nb_cols = self.nb_cols_input.value()
        nb_rows = self.nb_rows_input.value()
        grid_w = self.image_label.pixmap().width() / nb_cols
        grid_h = self.image_label.pixmap().height() / nb_rows
        col = int(x // grid_w)
        row = int(y // grid_h)
        if self.parent_controller:
            self.parent_controller.handle_place_product(col, row)