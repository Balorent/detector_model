# Import libraries
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from functools import partial
# Import files


class CustomSlider(QtWidgets.QFrame):
    def __init__(self, parent, pos, width, height, title_text, font_size, val_min, val_max, steps,
                 slider_width, slider_height):
        super().__init__(parent=parent)
        self.parent = parent

        # Dimensions
        self.width = width
        self.height = height
        self.pos = pos
        self.setGeometry(self.pos[0], self.pos[1], self.width, self.height)
        self.setFixedWidth(self.width)
        self.setFixedHeight(self.height)

        # Frame
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setAlignment(QtCore.Qt.AlignLeft)
        self.setStyleSheet("background-color : transparent")

        # Label
        self.title_text = title_text
        self.font_size = font_size
        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setText(self.title_text)
        self.title_label.setStyleSheet("font-size: " + str(self.font_size) + "pt;")
        self.title_label.setFixedWidth(10)
        self.layout().addWidget(self.title_label)

        # Slider
        self.val_min = val_min
        self.val_max = val_max
        self.steps = steps
        self.slider_width = slider_width
        self.slider_height = slider_height
        self.slider = QtWidgets.QSlider(self)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setFixedWidth(self.slider_width)
        self.slider.setFixedHeight(self.slider_height)
        self.slider.setStyleSheet('QSlider::handle:horizontal:hover {background-color: black;}')
        # self.slider.setEnabled(False)
        self.slider.setMinimum(0)
        self.slider.setMaximum(self.steps)
        self.layout().addWidget(self.slider)

        # Textbox
        self.textbox = QtWidgets.QLineEdit(self)
        self.textbox.setFixedWidth(60)
        self.textbox.setFixedHeight(self.slider_height)
        self.textbox.setStyleSheet('background-color : white')
        # self.textbox.setEnabled(False)
        self.layout().addWidget(self.textbox)
