from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtWidgets import QApplication
from view.main_view import MainView
from controller.MainController import MainController
import sys

def ask_password():
    correct_password = "root"
    password, ok = QInputDialog.getText(None, "Accès sécurisé", "Mot de passe :", echo=QLineEdit.Password)
    if not ok or password != correct_password:
        QMessageBox.critical(None, "Erreur", "Mot de passe incorrect. Fermeture.")
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ask_password()
    view = MainView()
    controller = MainController(view)
    view.show()
    sys.exit(app.exec_())
