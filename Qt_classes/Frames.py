# Frames.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
from PyQt5 import QtWidgets, QtCore
from functools import partial
import numpy as np
# Import files
from Qt_classes import Plots1D as myPlots1D
from Qt_classes import PolarPlots as myPolarPlots
from Qt_classes import Plots2D as myPlots2D
from Qt_classes import Buttons as myButtons
from Qt_classes import Sliders as mySliders
from Controller import buttons_controller as Bcontrol


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


class TitleFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color, title_text, font_size):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=None, shadow=None)
        self.layout().setAlignment(QtCore.Qt.AlignTop)
        self.layout().setSpacing(5)

        # Title
        self.title_text = title_text
        self.font_size = font_size
        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setText(self.title_text)
        self.title_label.setStyleSheet("font-weight: bold; font-size: " + str(self.font_size) + "pt;")
        self.layout().addWidget(self.title_label, alignment=QtCore.Qt.AlignCenter)

        # Content
        self.content_frame = CustomFrame(parent=self, pos=[0, 0], width=self.width,
                                         height=self.height-self.font_size-10, color='transparent',
                                         layout=QtWidgets.QGridLayout(), spacing=0, margins=[0, 0, 0, 0],
                                         shape=None, shadow=None)
        self.content_frame.setFixedHeight(self.content_frame.height)
        self.content_frame.setFixedWidth(self.content_frame.width)
        self.layout().addWidget(self.content_frame)

    def add_widget(self, widget, row, col):
        self.content_frame.layout().addWidget(widget, row, col)


class MainFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color, layout, spacing, margins, shape, shadow, title_text,
                 font_size):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=layout, spacing=spacing, margins=margins, shape=shape, shadow=shadow)
        self.title_frame = CustomFrame(parent=self, pos=(0, 0), width=self.width, height=15, color='#c4c4c4',
                                       layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                                       shape=QtWidgets.QFrame.StyledPanel, shadow=None)

        # Title
        self.title_text = title_text
        self.font_size = font_size
        self.title_label = QtWidgets.QLabel(self)
        self.title_label.setText(self.title_text)
        self.title_label.setStyleSheet("font-size: " + str(self.font_size) + "pt;")
        self.title_frame.layout().addWidget(self.title_label, alignment=QtCore.Qt.AlignLeft)

        # Button
        self.menu_button = myButtons.CustomButton(parent=self.title_frame, pos=(0, 0), width=self.title_frame.height,
                                                  height=self.title_frame.height, text='▼', font_size=10,
                                                  color='transparent', hover_color='blue')
        self.title_frame.layout().addWidget(self.menu_button, alignment=QtCore.Qt.AlignRight)

    def update_size(self, pos, width, height):
        super().update_size(pos, width, height)
        self.title_frame.update_size(pos=[0, 0], width=self.width, height=self.title_frame.height)


class SeparatorFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.VLine, shadow=None)
        self.setStyleSheet('QFrame {color : ' + color + '}')


class OptionFrame(CustomFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QHBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken)
        self.layout().setAlignment(QtCore.Qt.AlignLeft)

        # -------------- Scatterers options --------------
        self.scatterer_options_frame = TitleFrame(parent=self, pos=[0, 0], width=500, height=self.height,
                                                  color='transparent', title_text="Scatterers options", font_size=9)
        self.scatterer_options_frame.setFixedWidth(self.scatterer_options_frame.width)
        self.layout().addWidget(self.scatterer_options_frame)
        # Add button
        self.add_button = myButtons.CustomButton(parent=self, pos=[0, 0], width=75, height=28, text="Add",
                                                 font_size=10, color='light grey', hover_color='grey')
        self.scatterer_options_frame.add_widget(widget=self.add_button, row=0, col=0)
        self.add_button.clicked.connect(partial(Bcontrol.add_random, parent, 1))
        # Remove all button
        self.remove_all_button = myButtons.CustomButton(parent=self, pos=[0, 0], width=75, height=28,
                                                        text="Remove all", font_size=10, color='light grey',
                                                        hover_color='grey')
        self.scatterer_options_frame.add_widget(widget=self.remove_all_button, row=1, col=0)
        self.remove_all_button.clicked.connect(partial(Bcontrol.remove_all, parent))
        # X slider
        self.x_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='x',
                                               font_size=9, val_min=-10, val_max=10, steps=2000, slider_width=100,
                                               slider_height=20)
        self.scatterer_options_frame.add_widget(widget=self.x_slider, row=0, col=1)
        # Y slider
        self.y_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='y',
                                               font_size=9, val_min=-10, val_max=10, steps=2000, slider_width=100,
                                               slider_height=20)
        self.scatterer_options_frame.add_widget(widget=self.y_slider, row=1, col=1)
        # R slider
        self.r_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='r',
                                               font_size=9, val_min=0, val_max=10, steps=2000, slider_width=100,
                                               slider_height=20)
        self.scatterer_options_frame.add_widget(widget=self.r_slider, row=0, col=2)
        # Theta slider
        self.theta_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='\u03B8',
                                                   font_size=9, val_min=0, val_max=2*np.pi, steps=2000,
                                                   slider_width=100, slider_height=20)
        self.scatterer_options_frame.add_widget(widget=self.theta_slider, row=1, col=2)
        # Separator
        self.scatterer_options_sep = SeparatorFrame(parent=self, pos=[0, 0], width=1, height=self.height,
                                                    color='grey')
        self.scatterer_options_sep.setFixedWidth(self.scatterer_options_sep.width)
        self.layout().addWidget(self.scatterer_options_sep)

        # -------------- Wave options --------------
        self.wave_options_frame = TitleFrame(parent=self, pos=[0, 0], width=200, height=self.height,
                                             color='transparent', title_text="Wave options", font_size=9)
        self.wave_options_frame.setFixedWidth(self.wave_options_frame.width)
        self.layout().addWidget(self.wave_options_frame)
        # k slider
        self.k_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='k',
                                               font_size=9, val_min=0, val_max=10, steps=2000, slider_width=100,
                                               slider_height=20)
        self.wave_options_frame.add_widget(widget=self.k_slider, row=0, col=0)
        # lambda slider
        self.lambda_slider = mySliders.CustomSlider(parent=self, pos=[0, 0], width=200, height=40, title_text='\u03BB',
                                                    font_size=9, val_min=0, val_max=10, steps=2000, slider_width=100,
                                                    slider_height=20)
        self.wave_options_frame.add_widget(widget=self.lambda_slider, row=1, col=0)
        # Separator
        self.wave_options_sep = SeparatorFrame(parent=self, pos=[0, 0], width=1, height=self.height,
                                                    color='grey')
        self.wave_options_sep.setFixedWidth(self.wave_options_sep.width)
        self.layout().addWidget(self.wave_options_sep)


class ObstacleFrame(MainFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken,
                         title_text="Obstacles", font_size=9)


class XYFrame(MainFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken,
                         title_text="Wave function", font_size=9)

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


class DirectionalityFrame(MainFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken,
                         title_text="Directionality", font_size=9)

        self.graph = myPlots1D.DirectionalityPlot(parent=self, plot_color='w', frame_color="transparent", line1_color='b',
                                                  line2_color='r', axis_color='k', ticks_color='k', text_color='k',
                                                  x_label="step", y_label="R")
        self.layout().addWidget(self.graph)


class ThetaFrame(MainFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken,
                         title_text="Polar plot", font_size=9)

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
        # self.graph = myPolarPlots.PolarPlot(parent=self, plot_color='w', frame_color="transparent", line1_color='b',
        #                                     line2_color='r', axis_color='k', ticks_color='k', text_color='k',
        #                                     x_label="\u03B8 [rad]", y_label="J(\u03B8) [k]")
        self.graph = myPlots1D.ThetaPlot(parent=self, plot_color='w', frame_color="transparent", line1_color='b',
                                         line2_color='r', axis_color='k', ticks_color='k', text_color='k',
                                         x_label="\u03B8 [rad]", y_label="J(\u03B8) [k]")
        self.plot_frame.layout().addWidget(self.graph)

    def update_size(self, pos, width, height):
        super().update_size(pos, width, height)
        self.top_frame.update_size(pos=[0, 0], width=self.width, height=self.top_frame.height)
        self.plot_frame.update_size(pos=[0, self.top_frame.height], width=self.width,
                                    height=self.height - self.top_frame.height)


class ResFrame(MainFrame):
    def __init__(self, parent, pos, width, height, color):
        super().__init__(parent=parent, pos=pos, width=width, height=height, color=color,
                         layout=QtWidgets.QVBoxLayout(), spacing=0, margins=[0, 0, 0, 0],
                         shape=QtWidgets.QFrame.StyledPanel, shadow=QtWidgets.QFrame.Sunken,
                         title_text="Resonances", font_size=9)

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
