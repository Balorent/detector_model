# Window.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut
from functools import partial
# Import files
from Qt_classes import Frames as myFrames
from Controller import shortcut_controller as ShControl


class Window(QtWidgets.QMainWindow):
    def __init__(self, app):
        super().__init__()

        # Dimensions
        self.screen_width = QtWidgets.QDesktopWidget().availableGeometry().width()
        self.screen_height = QtWidgets.QDesktopWidget().availableGeometry().height()
        self.width = int(self.screen_width/1.1)
        self.height = int((self.screen_height-30)/1.1)
        self.setGeometry(int((self.screen_width - self.width)/2),
                         int((self.screen_height - self.height)/2),
                         self.width,
                         self.height)
        self.padding = 5

        # Colors
        self.win_color = 'white'
        self.frame_color = '#dbdbdb'
        self.setStyleSheet("background-color : " + self.win_color)

        # Option frame
        self.option_height = 95
        self.option_frame = myFrames.OptionFrame(parent=self, pos=[self.padding, 0], width=self.width - 2*self.padding,
                                                 height=self.option_height, color=self.frame_color)

        # XY frame
        self.XY_frame = myFrames.XYFrame(parent=self, pos=[self.padding, self.option_frame.height + self.padding],
                                         width=self.height - self.option_frame.height - 2*self.padding,
                                         height=self.height - self.option_frame.height - 2*self.padding,
                                         color=self.frame_color)

        # Theta frame
        self.Theta_frame = myFrames.ThetaFrame(parent=self,
                                               pos=[self.XY_frame.width + 2*self.padding,
                                                    self.option_frame.height + self.padding],
                                               width=self.width - self.XY_frame.width - 3*self.padding,
                                               height=int((self.height - self.option_frame.height - 3*self.padding)/2),
                                               color=self.frame_color)

        # Res frame
        self.Res_frame = myFrames.ResFrame(parent=self,
                                           pos=[self.XY_frame.width + 2*self.padding,
                                                self.option_frame.height + self.Theta_frame.height + 2*self.padding],
                                           width=self.width - self.XY_frame.width - 3*self.padding,
                                           height=int((self.height - self.option_frame.height - 3*self.padding)/2),
                                           color=self.frame_color)

        # Shortcuts
        QShortcut(QKeySequence(QtCore.Qt.Key_Backspace), self).activated.connect(partial(ShControl.remove_selected, self))

    def resizeEvent(self, event):
        self.width = self.geometry().width()
        self.height = self.geometry().height()
        self.option_frame.update_size(pos=[self.padding, 0], width=self.width - 2*self.padding, height=self.option_height)
        self.XY_frame.update_size(pos=[self.padding, self.option_frame.height + self.padding],
                                  width=self.height - self.option_frame.height - 2*self.padding,
                                  height=self.height - self.option_frame.height - 2*self.padding)
        self.Theta_frame.update_size(pos=[self.XY_frame.width + 2*self.padding,
                                          self.option_frame.height + self.padding],
                                     width=self.width - self.XY_frame.width - 3*self.padding,
                                     height=int((self.height - self.option_frame.height - 3*self.padding)/2))
        self.Res_frame.update_size(pos=[self.XY_frame.width + 2*self.padding,
                                        self.option_frame.height + self.Theta_frame.height + 2*self.padding],
                                   width=self.width - self.XY_frame.width - 3*self.padding,
                                   height=int((self.height - self.option_frame.height - 3*self.padding)/2))
