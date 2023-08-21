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
        self.brush = [self.normal_brush_color for i in range(parameters.N)]
        self.setBrush(self.brush)

        # Pen
        self.normal_pen_color = 'k'
        self.highlighted_pen_color = 'w'
        self.selected_pen_color = 'w'
        self.pen = [self.normal_pen_color for i in range(parameters.N)]
        self.setPen(self.pen)

        # Size
        self.size = 8
        self.setSize(8)

        # Snip distance
        self.snip_dist = (parameters.x_max - parameters.x_min) / 75

        # Lists
        self.highlighted = [False for i in range(parameters.N)]
        self.selected = [False for i in range(parameters.N)]

        # Movement
        self.on_move = False

    def highlight(self, i):
        self.brush[i] = self.highlighted_brush_color
        self.setBrush(self.brush)
        self.pen[i] = self.highlighted_pen_color
        self.setPen(self.pen)
        self.highlighted[i] = True

    def unhighlight(self, i):
        self.brush[i] = self.normal_brush_color
        self.setBrush(self.brush)
        self.pen[i] = self.normal_pen_color
        self.setPen(self.pen)
        self.highlighted[i] = False

    def is_highlighted(self, i):
        return self.highlighted[i]

    def select(self, i):
        self.brush[i] = self.selected_brush_color
        self.setBrush(self.brush)
        self.pen[i] = self.selected_pen_color
        self.setPen(self.pen)
        self.selected[i] = True

    def deselect(self, i):
        self.brush[i] = self.normal_brush_color
        self.setBrush(self.brush)
        self.pen[i] = self.normal_pen_color
        self.setPen(self.pen)
        self.selected[i] = False

    def is_selected(self, i):
        return self.selected[i]
