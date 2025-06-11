import sys
from PyQt5.QtWidgets import QApplication
from controller.controller_app2 import ControllerApp2

if name == "main":
app = QApplication(sys.argv)
controller = ControllerApp2()
controller.run()
sys.exit(app.exec_())
