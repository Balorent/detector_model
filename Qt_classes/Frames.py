# Frames.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
from PyQt5 import QtWidgets, QtCore
# Import files
from Qt_classes import Plots1D as myPlots1D
from Qt_classes import Plots2D as myPlots2D


class CustomFrame(QtWidgets.QFrame):
    def __init__(self, parent, pos, width, height, color, layout, spacing, margins, shape, shadow):
        super().__init__(parent=parent)
        self.parent = parent

        # Dimensions
        self.width = width
        self.height = height
        self.pos = pos
        self.setGeometry(self.pos[0], self.pos[1], self.width, self.height)

        # Colors
        self.color = color
        self.setStyleSheet("background-color : " + self.color)

        # Organization
        self.layout_type = layout
        self.spacing = spacing
        self.margins = margins
        self.setLayout(self.layout_type)
        self.layout().setSpacing(self.spacing)
        self.layout().setContentsMargins(self.margins[0], self.margins[1], self.margins[2], self.margins[3])

        # Style
        self.shape = shape
        self.shadow = shadow
        if self.shape is not None:
            self.setFrameShape(self.shape)
        if self.shadow is not None:
            self.setFrameShadow(self.shadow)

    def update_size(self, pos, width, height):
        self.width = width
        self.height = height
        self.pos = pos
        self.setGeometry(self.pos[0], self.pos[1], self.width, self.height)


class OptionFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken)


class XYFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken)

        # Top frame
        self.top_frame = CustomFrame(parent=self, pos=[0, 0], width=self.width, height=115, color='transparent',
                                     layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                     shape=None, shadow=None)
        self.top_frame.setFixedHeight(self.top_frame.height)
        self.layout().addWidget(self.top_frame)

        # Plot frame
        self.plot_frame = CustomFrame(parent=self, pos=[0, self.top_frame.height], width=self.width,
                                      height=self.height - self.top_frame.height, color='transparent',
                                      layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                      shape=None, shadow=None)
        self.layout().addWidget(self.plot_frame)
        self.graph = myPlots2D.XYPlot(parent=self, plot_color='k', frame_color='transparent', axis_color='k',
                                      ticks_color='w', text_color='k', x_label='x', y_label='y')
        self.plot_frame.layout().addWidget(self.graph.image_view)

    def update_size(self, pos, width, height):
        super().update_size(pos, width, height)
        self.top_frame.update_size(pos=[0, 0], width=self.width, height=self.top_frame.height)
        self.plot_frame.update_size(pos=[0, self.top_frame.height], width=self.width,
                                    height=self.height - self.top_frame.height)


class ThetaFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken)

        # Top frame
        self.top_frame = CustomFrame(parent=self, pos=[0, 0], width=self.width, height=75, color='transparent',
                                     layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                     shape=None, shadow=None)
        self.top_frame.setFixedHeight(self.top_frame.height)
        self.layout().addWidget(self.top_frame)

        # Plot frame
        self.plot_frame = CustomFrame(parent=self, pos=[0, self.top_frame.height], width=self.width,
                                      height=self.height - self.top_frame.height, color='transparent',
                                      layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                      shape=None, shadow=None)
        self.layout().addWidget(self.plot_frame)
        self.graph = myPlots1D.ThetaPlot(parent=self, plot_color='w', frame_color="transparent", line1_color='b',
                                         line2_color='r', axis_color='k', ticks_color='k', text_color='k',
                                         x_label="\u03B8 [rad]", y_label="J(\u03B8) [k]")
        self.plot_frame.layout().addWidget(self.graph)

    def update_size(self, pos, width, height):
        super().update_size(pos, width, height)
        self.top_frame.update_size(pos=[0, 0], width=self.width, height=self.top_frame.height)
        self.plot_frame.update_size(pos=[0, self.top_frame.height], width=self.width,
                                    height=self.height - self.top_frame.height)


class ResFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken)

        # Top frame
        self.top_frame = CustomFrame(parent=self, pos=[0, 0], width=self.width, height=75,
                                     color='transparent', layout=QtWidgets.QHBoxLayout(), spacing=0,
                                     margins=[0, 0, 0, 0], shape=None, shadow=None)
        self.top_frame.setFixedHeight(self.top_frame.height)
        self.layout().addWidget(self.top_frame)

        # Plot frame
        self.plot_frame = CustomFrame(parent=self, pos=[0, self.top_frame.height], width=self.width,
                                      height=self.height - self.top_frame.height, color='transparent',
                                      layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                      shape=None, shadow=None)
        self.layout().addWidget(self.plot_frame)

    def update_size(self, pos, width, height):
        super().update_size(pos, width, height)
        self.top_frame.update_size(pos=[0, 0], width=self.width, height=self.top_frame.height)
        self.plot_frame.update_size(pos=[0, self.top_frame.height], width=self.width,
                                    height=self.height - self.top_frame.height)
