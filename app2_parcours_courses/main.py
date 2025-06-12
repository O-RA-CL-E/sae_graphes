from PyQt5.QtWidgets import QApplication
from view.main_view import MainView
from controller.MainController import MainController
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = MainView()
    controller = MainController(view)
    view.show()
    sys.exit(app.exec_())
