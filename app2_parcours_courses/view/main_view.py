from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QListWidget, QVBoxLayout, QHBoxLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt

class MainView(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Parcours Courses")

        # Main horizontal layout
        main_layout = QHBoxLayout()

        # Left vertical layout: load button, plan, products list, buttons
        left_layout = QVBoxLayout()
        self.load_btn = QPushButton("Charger un magasin")
        self.load_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.plan_label = QLabel("Plan du magasin")
        self.plan_label.setAlignment(Qt.AlignCenter)
        self.products_list = QListWidget()
        self.products_list.setStyleSheet("font-size: 13px;")
        self.generate_random_list_btn = QPushButton("Générer une liste de courses aléatoire")
        self.generate_random_list_btn.setStyleSheet("font-size: 14px; padding: 8px;")
        self.shortest_path_btn = QPushButton("Tracer le chemin le plus court")
        self.shortest_path_btn.setStyleSheet("font-size: 14px; padding: 8px;")

        left_layout.addWidget(self.load_btn)
        left_layout.addWidget(self.plan_label)
        left_layout.addWidget(QLabel("Produits disponibles"))
        left_layout.addWidget(self.products_list)
        left_layout.addWidget(self.generate_random_list_btn)
        left_layout.addWidget(self.shortest_path_btn)

        # Right vertical layout: shopping list
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Liste de courses"))
        self.courses_list = QListWidget()
        self.courses_list.setStyleSheet("font-size: 13px;")
        right_layout.addWidget(self.courses_list)

        # Add left and right layouts to main layout
        main_layout.addLayout(left_layout, 3)
        main_layout.addLayout(right_layout, 1)

        # Set margins and spacing
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        left_layout.setSpacing(10)
        right_layout.setSpacing(10)

        self.setLayout(main_layout)

    def afficher_plan_avec_grille(self, image_path, nb_cols, nb_rows, produits=None, chemin=None):
        import os
        full_path = os.path.join("projets", image_path) if not os.path.isabs(image_path) else image_path
        if not os.path.exists(full_path):
            self.plan_label.setText("Image non trouvée")
            return
        pixmap = QPixmap(full_path)
        pixmap = pixmap.scaled(800, 800, Qt.KeepAspectRatio)
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
            for prod in produits:
                col = prod.get("col", 0)
                row = prod.get("row", 0)
                x = int(col * width / nb_cols)
                y = int(row * height / nb_rows)
                color = prod.get("color", "blue")
                if color == "red":
                    pen = QPen(Qt.red, 3)
                else:
                    pen = QPen(Qt.blue, 3)
                painter.setPen(pen)
                painter.drawEllipse(x+2, y+2, int(width/nb_cols)-4, int(height/nb_rows)-4)
                painter.drawText(x+5, y+20, prod.get("label", ""))
        # Affichage du chemin
        if chemin is not None and len(chemin) > 0:
            from math import atan2, cos, sin, pi
            from PyQt5.QtCore import QPointF
            pen = QPen(Qt.green, 2)
            painter.setPen(pen)
            prev_x, prev_y = None, None
            arrow_size = 10
            for i, point in enumerate(chemin):
                col = point.get("col", 0)
                row = point.get("row", 0)
                x = int(col * width / nb_cols) + int(width / (2 * nb_cols))
                y = int(row * height / nb_rows) + int(height / (2 * nb_rows))
                if prev_x is not None and prev_y is not None:
                    # Draw line
                    painter.drawLine(prev_x, prev_y, x, y)
                    # Draw arrowhead
                    angle = atan2(y - prev_y, x - prev_x)
                    arrow_p1 = (x - arrow_size * cos(angle - pi / 6), y - arrow_size * sin(angle - pi / 6))
                    arrow_p2 = (x - arrow_size * cos(angle + pi / 6), y - arrow_size * sin(angle + pi / 6))
                    points = [QPointF(x, y), QPointF(*arrow_p1), QPointF(*arrow_p2)]
                    painter.setBrush(Qt.green)
                    painter.drawPolygon(*points)
                prev_x, prev_y = x, y
        painter.end()
        self.plan_label.setPixmap(pixmap)
