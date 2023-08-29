# Scatterers.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
import pyqtgraph as pg
import numpy as np
# Import files
import parameters


class Scatterers(pg.ScatterPlotItem):
    def __init__(self, pos):
        super().__init__()
        self.setData(pos=pos)

        # Brush
        self.normal_brush_color = 'w'
        self.highlighted_brush_color = 'k'
        self.selected_brush_color = 'r'
        self.brush = np.array([self.normal_brush_color for i in range(parameters.N)])
        self.setBrush(self.brush)

        # Pen
        self.normal_pen_color = 'k'
        self.highlighted_pen_color = 'w'
        self.selected_pen_color = 'w'
        self.pen = np.array([self.normal_pen_color for i in range(parameters.N)])
        self.setPen(self.pen)

        # Size
        self.size = 8
        self.setSize(8)

        # Snip distance
        self.snip_dist = (parameters.x_max - parameters.x_min) / 75

        # State : 0=normal ; 1=highlighted ; 2=selected
        self.state = np.array([0 for i in range(parameters.N)])

        # Momentum
        self.momentum = np.random.random((parameters.N, 2)) * 0.1

    def update_color(self):
        self.brush = np.select([self.state == 0,         self.state == 1,              self.state == 2],
                               [self.normal_brush_color, self.highlighted_brush_color, self.selected_brush_color])
        self.setBrush(self.brush)
        self.pen = np.select([self.state == 0,       self.state == 1,            self.state == 2],
                             [self.normal_pen_color, self.highlighted_pen_color, self.selected_pen_color])
        self.setPen(self.pen)

    def add_scatterer(self):
        self.setData(pos=parameters.coordinates)
        self.brush = np.append(self.brush, self.normal_brush_color)
        self.setBrush(self.brush)
        self.pen = np.append(self.pen, self.normal_pen_color)
        self.setPen(self.pen)
        self.state = np.append(self.state, 0)
        self.momentum = np.append(self.momentum, np.random.random((1, 2)) * 0.1)

    def remove_scatterer(self, index):
        self.setData(pos=parameters.coordinates)
        self.brush = np.delete(self.brush, index)
        self.setBrush(self.brush)
        self.pen = np.delete(self.pen, index)
        self.setPen(self.pen)
        self.state = np.delete(self.state, index)
        self.momentum = np.delete(self.momentum, index)

    def remove_all_scatterers(self):
        self.setData(pos=parameters.coordinates)
        self.brush = np.zeros(0)
        self.setBrush(self.brush)
        self.pen = np.zeros(0)
        self.setPen(self.pen)
        self.state = np.zeros(0)
        self.momentum = np.zeros((0, 2))
