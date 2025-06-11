from PyQt5.QtWidgets import QMainWindow, QPushButton, QListWidget, QGraphicsScene, QGraphicsView
from PyQt5.QtGui import QPixmap, QBrush, QColor
from PyQt5.QtCore import QRectF

class FenetreApp2(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Application 2 - Parcours de Courses")
        self.setGeometry(100, 100, 1200, 700)
        self.init_ui()

    def init_ui(self):
        self.btn_charger = QPushButton("Charger un projet", self)
        self.btn_charger.setGeometry(20, 20, 200, 40)

        self.btn_generer = QPushButton("Générer une liste de courses", self)
        self.btn_generer.setGeometry(20, 70, 200, 40)

        self.liste_widget = QListWidget(self)
        self.liste_widget.setGeometry(20, 130, 200, 500)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene, self)
        self.view.setGeometry(250, 20, 900, 650)

    def afficher_plan(self, image_path):
        self.scene.clear()
        pixmap = QPixmap(image_path)
        self.scene.addPixmap(pixmap)

    def maj_liste_courses(self, produits):
        self.liste_widget.clear()
        for p in produits:
            self.liste_widget.addItem(p['nom'])

    def afficher_produits(self, produits, grille_info, couleur='blue'):
        couleur_qt = QColor(couleur)
        taille_case = grille_info.get('taille', 40)
        origine_x, origine_y = grille_info.get('origine', [0, 0])

        for p in produits:
            x_pix = origine_x + p['x'] * taille_case
            y_pix = origine_y + p['y'] * taille_case
            ellipse = self.scene.addEllipse(QRectF(x_pix - 5, y_pix - 5, 10, 10))
            ellipse.setBrush(QBrush(couleur_qt))
            ellipse.setZValue(1)

