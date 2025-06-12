from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parcours Courses")
        self.layout = QVBoxLayout()
        self.load_btn = QPushButton("Charger un magasin")
        self.plan_label = QLabel("Plan du magasin")
        self.products_list = QListWidget()
        self.courses_list = QListWidget()
        self.layout.addWidget(self.load_btn)
        self.layout.addWidget(self.plan_label)
        self.layout.addWidget(QLabel("Produits disponibles"))
        self.layout.addWidget(self.products_list)
        self.layout.addWidget(QLabel("Liste de courses"))
        self.layout.addWidget(self.courses_list)
        self.setLayout(self.layout)

    def afficher_plan_avec_grille(self, image_path, nb_cols, nb_rows, produits=None):
        import os
        full_path = os.path.join("projets", image_path) if not os.path.isabs(image_path) else image_path
        if not os.path.exists(full_path):
            self.plan_label.setText("Image non trouvée")
            return
        pixmap = QPixmap(full_path)
        pixmap = pixmap.scaled(400, 400, Qt.KeepAspectRatio)
        painter = QPainter(pixmap)
        pen = QPen(Qt.red, 1)
        painter.setPen(pen)
        width = pixmap.width()
        height = pixmap.height()
        # Quadrillage
        for col in range(nb_cols + 1):
            x = int(col * width / nb_cols)
            painter.drawLine(x, 0, x, height)
        for row in range(nb_rows + 1):
            y = int(row * height / nb_rows)
            painter.drawLine(0, y, width, y)
        # Affichage des produits de la liste de courses
        if produits is not None:
            pen = QPen(Qt.blue, 3)
            painter.setPen(pen)
            for prod in produits:
                col = prod.get("col", 0)
                row = prod.get("row", 0)
                x = int(col * width / nb_cols)
                y = int(row * height / nb_rows)
                painter.drawEllipse(x+2, y+2, int(width/nb_cols)-4, int(height/nb_rows)-4)
                painter.drawText(x+5, y+20, prod.get("label", ""))
        painter.end()
        self.plan_label.setPixmap(pixmap)