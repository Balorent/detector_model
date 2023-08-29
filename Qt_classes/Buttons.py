# Import libraries
from PyQt5 import QtWidgets, QtCore
# Import files


class CustomButton(QtWidgets.QPushButton):
    def __init__(self, parent, pos, width, height, text, color, hover_color):
        super().__init__(parent=parent, text=text)
        self.parent = parent

        # Dimensions
        self.width = width
        self.height = height
        self.pos = pos
        self.setGeometry(self.pos[0], self.pos[1], self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        # Colors
        self.setStyleSheet('QPushButton {background-color: ' + color + '};')
