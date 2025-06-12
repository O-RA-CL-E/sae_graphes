from model.magasin import Magasin

class MainController:
    def __init__(self, view):
        self.view = view
        self.magasin = None
        self.view.load_btn.clicked.connect(self.charger_magasin)
        self.view.products_list.itemDoubleClicked.connect(self.ajouter_a_courses)

    def charger_magasin(self):
        from PyQt5.QtWidgets import QFileDialog
        path, _ = QFileDialog.getOpenFileName(self.view, "Charger un magasin", "", "JSON (*.json)")
        if path:
            try:
                self.magasin = Magasin(path)
                self.view.afficher_plan_avec_grille(
                    self.magasin.image_path,
                    self.magasin.nb_cols,
                    self.magasin.nb_rows
                )
                self.view.products_list.clear()
                for prod in self.magasin.products:
                    nom = prod.get("label", "Produit sans nom")
                    self.view.products_list.addItem(nom)
            except Exception as e:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self.view, "Erreur", f"Erreur lors du chargement : {e}")
        self.view.afficher_plan_avec_grille(
        self.magasin.image_path,
        self.magasin.nb_cols,
        self.magasin.nb_rows
)

    def ajouter_a_courses(self, item):
        self.view.courses_list.addItem(item.text())