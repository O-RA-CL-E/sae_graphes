from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox
import sys

from model.project_model import ProjectModel
from view.project_view import ProjectView
from controller.project_controller import ProjectController

def ask_password():
    correct_password = "root"
    password, ok = QInputDialog.getText(None, "Accès sécurisé", "Mot de passe :", echo=QInputDialog.Password)
    if not ok or password != correct_password:
        QMessageBox.critical(None, "Erreur", "Mot de passe incorrect. Fermeture.")
    sys.exit()

def main():
    app = QApplication(sys.argv)
    ask_password()

model = ProjectModel()
view = ProjectView()
controller = ProjectController(model, view)

view.show()
sys.exit(app.exec_())

if name == "main":
    main()