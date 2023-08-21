# Plots2D.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np

import Math
# Import files
import parameters
import Qt_classes.Scatterers as myScatterers


class Custom2DPlot(pg.PlotItem):
    def __init__(self, parent, plot_color, frame_color, axis_color, ticks_color, text_color, x_label, y_label, x_min, x_max, x_res,
                 y_min, y_max, y_res):
        super().__init__()
        self.parent=parent

        # Colors
        self.plot_color = plot_color
        self.frame_color = frame_color
        self.axis_color = axis_color
        self.ticks_color = ticks_color
        self.text_color = text_color
        pg.setConfigOption('background', self.frame_color)
        self.getViewBox().setBackgroundColor(self.plot_color)

        # Axis
        for orientation in ["bottom", "right", "top", "left"]:
            self.showAxis(orientation)
            axis = self.getAxis(orientation)
            axis.setPen(pg.mkPen(self.axis_color))
            axis.setTextPen(pg.mkPen(self.text_color))
            axis.setTickPen(pg.mkPen(self.ticks_color))

        # Axis labels
        self.x_label = x_label
        self.y_label = y_label
        self.style = {"color": "black", "font-size": "13px"}
        self.setLabel("bottom", self.x_label, **self.style)
        self.setLabel("left", self.y_label, **self.style)

        # Grid
        self.addItem(pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen('w', width=0.75)))
        self.addItem(pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen('w', width=0.75)))
        self.showGrid(x=True, y=True, alpha=0.1)

        # Ranges
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.setXRange(self.x_min, self.x_max)
        self.setYRange(self.y_min, self.y_max)
        self.view_range = self.getViewBox().viewRange()
        self.x_min, self.x_max = self.view_range[0][0], self.view_range[0][1]
        self.y_min, self.y_max = self.view_range[1][0], self.view_range[1][1]

        # Resolution
        self.x_res, self.y_res = x_res, y_res

        # Mesh
        self.mesh = np.meshgrid(np.linspace(self.y_min, self.y_max, self.y_res),
                                np.linspace(self.x_min, self.x_max, self.x_res))

        # Image View
        self.image_view = pg.ImageView(view=self)
        self.image_view.ui.roiBtn.hide()
        self.image_view.ui.menuBtn.hide()

        # Connect signals
        self.getViewBox().sigRangeChanged.connect(self.range_changed)

    def range_changed(self, event):
        self.view_range = self.getViewBox().viewRange()
        self.x_min, self.x_max = self.view_range[0][0], self.view_range[0][1]
        self.y_min, self.y_max = self.view_range[1][0], self.view_range[1][1]
        self.mesh = np.meshgrid(np.linspace(self.y_min, self.y_max, self.y_res),
                                np.linspace(self.x_min, self.x_max, self.x_res))


class XYPlot(Custom2DPlot):
    def __init__(self, parent, plot_color, frame_color, axis_color, ticks_color, text_color, x_label, y_label):
        super().__init__(parent=parent, plot_color=plot_color, frame_color=frame_color, axis_color=axis_color,
                         ticks_color=ticks_color, text_color=text_color, x_label=x_label, y_label=y_label,
                         x_min=parameters.x_min, x_max=parameters.x_max, x_res=parameters.x_res, y_min=parameters.y_min,
                         y_max=parameters.y_max, y_res=parameters.y_res)

        # Data
        self.data = np.log(np.abs(Math.compute_psi(self.mesh[1], self.mesh[0], False)))
        self.image_view.setImage(self.data,
                                 pos=(self.x_min, self.y_min),
                                 scale=((self.x_max - self.x_min) / self.x_res, (self.y_max - self.y_min) / self.y_res),
                                 autoRange=False)

        # Scatterers
        self.scatterers = myScatterers.Scatterers(parameters.coordinates)
        self.addItem(self.scatterers)

        # color_bar
        self.color_bar = self.image_view.ui.histogram
        self.custom_colors = [(0, 0, 0), (0, 0, 128), (0, 0, 255), (0, 128, 255),
                              (0, 255, 255), (128, 255, 128), (255, 255, 0),
                              (255, 128, 0), (255, 0, 0), (128, 0, 0)]
        self.custom_color_map = pg.ColorMap(np.linspace(0, 1, len(self.custom_colors)), self.custom_colors)
        self.color_bar.gradient.setColorMap(self.custom_color_map)

        # Connect signals
        self.getViewBox().scene().sigMouseMoved.connect(self.mouse_moved)
        self.getViewBox().scene().sigMouseClicked.connect(self.mouse_clicked)

    def mouse_moved(self, event):
        pos = self.mapToView(event)  # Get position of mouse
        x, y = pos.x(), pos.y()
        for (i, [xi, yi]) in enumerate(parameters.coordinates):
            if not self.scatterers.is_selected(i):
                if np.sqrt((xi - x) ** 2 + (yi - y) ** 2) < self.scatterers.snip_dist:
                    if not self.scatterers.is_highlighted(i):
                        self.scatterers.highlight(i)
                elif self.scatterers.is_highlighted(i):
                    self.scatterers.unhighlight(i)
            elif self.scatterers.is_selected(i):
                parameters.coordinates[i] = [x, y]
                self.scatterers.setData(pos=parameters.coordinates,
                                        brush=self.scatterers.brush,
                                        pen=self.scatterers.pen)
                self.data = np.log(np.abs(Math.compute_psi(self.mesh[1], self.mesh[0], True)))
                self.image_view.setImage(self.data,
                                         pos=(self.x_min, self.y_min),
                                         scale=((self.x_max - self.x_min) / self.x_res,
                                                (self.y_max - self.y_min) / self.y_res),
                                         autoRange=False, autoLevels=False)
                self.parent.parent.Theta_frame.graph.plot_line1()

    def mouse_clicked(self, event):
        for (i, [xi, yi]) in enumerate(parameters.coordinates):
            if self.scatterers.is_highlighted(i):
                if not self.scatterers.is_selected(i):
                    self.scatterers.unhighlight(i)
                    self.scatterers.select(i)
            elif self.scatterers.is_selected(i):
                self.scatterers.deselect(i)

    def range_changed(self, event):
        super().range_changed(event)
        self.data = np.log(np.abs(Math.compute_psi(self.mesh[1], self.mesh[0], False)))
        self.image_view.setImage(self.data,
                                 pos=(self.x_min, self.y_min),
                                 scale=((self.x_max - self.x_min) / self.x_res, (self.y_max - self.y_min) / self.y_res),
                                 autoRange=False, autoLevels=False)
        parameters.x_min = self.x_min
        parameters.x_max = self.x_max
        parameters.y_min = self.y_min
        parameters.y_max = self.y_max
        self.scatterers.snip_dist = (parameters.x_max - parameters.x_min) / 75
