import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from model.project_model import ProjectModel
from view.project_view import ProjectView
from controller.project_controller import ProjectController

class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Connexion")
        self.setFixedSize(300, 150)
        layout = QVBoxLayout()

        self.label = QLabel("Mot de passe :")
        layout.addWidget(self.label)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Se connecter")
        self.login_button.clicked.connect(self.check_password)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_password(self):
        if self.password_input.text() == "root":
            self.accept()
        else:
            QMessageBox.warning(self, "Erreur", "Mot de passe incorrect.")

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    if login_window.exec_() == QDialog.Accepted:
        model = ProjectModel()
        view = ProjectView()
        controller = ProjectController(model, view)
        view.show()
        sys.exit(app.exec_())

if __name__ == "__main__":
    main()