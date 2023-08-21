# main.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
import sys
from PyQt5 import QtWidgets
# Import files
from Qt_classes import Window as myWindow
import Controller.initialize as init
import Math

init.init_scatterers()
Math.update_math()
app = QtWidgets.QApplication(sys.argv)
window = myWindow.Window(app=app)
window.show()
sys.exit(app.exec_())
