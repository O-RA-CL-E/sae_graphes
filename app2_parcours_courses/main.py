<<<<<<< HEAD
from PyQt5.QtWidgets import QApplication, QInputDialog, QMessageBox, QLineEdit
=======
from PyQt5.QtWidgets import QApplication
>>>>>>> ba53c75e740cbf5f8e9ee729d564d80d70ce5ed1
from view.main_view import MainView
from controller.MainController import MainController
import sys

<<<<<<< HEAD
def ask_password():
    correct_password = "root"
    password, ok = QInputDialog.getText(None, "Accès sécurisé", "Mot de passe :", echo=QLineEdit.Password)
    if not ok or password != correct_password:
        QMessageBox.critical(None, "Erreur", "Mot de passe incorrect. Fermeture.")
        sys.exit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ask_password()
=======
if __name__ == "__main__":
    app = QApplication(sys.argv)
>>>>>>> ba53c75e740cbf5f8e9ee729d564d80d70ce5ed1
    view = MainView()
    controller = MainController(view)
    view.show()
    sys.exit(app.exec_())
