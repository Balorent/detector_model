# Plots1D.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
import pyqtgraph as pg
import numpy as np

import Math
# Import files
import parameters


class Custom1DPlot(pg.PlotWidget):
    def __init__(self, parent, plot_color, frame_color, line1_color, line2_color, axis_color, ticks_color, text_color, x_label,
                 y_label):
        super().__init__()
        self.parent = parent

        # Colors
        self.plot_color = plot_color
        self.frame_color = frame_color
        self.line1_color = line1_color
        self.line2_color = line2_color
        self.axis_color = axis_color
        self.ticks_color = ticks_color
        self.text_color = text_color
        self.setBackground(self.frame_color)
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
        self.addItem(pg.InfiniteLine(pos=0, angle=90, pen=pg.mkPen(self.axis_color, width=0.75)))
        self.addItem(pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(self.axis_color, width=0.75)))
        self.addItem(pg.InfiniteLine(pos=2*np.pi, angle=90, pen=pg.mkPen(self.axis_color, width=0.75)))
        self.showGrid(x=True, y=True, alpha=0.1)


class ThetaPlot(Custom1DPlot):
    def __init__(self, parent, plot_color, frame_color, line1_color, line2_color, axis_color, ticks_color, text_color, x_label,
                 y_label):
        super().__init__(parent=parent, plot_color=plot_color, frame_color=frame_color, line1_color=line1_color,
                         line2_color=line2_color, axis_color=axis_color, ticks_color=ticks_color,
                         text_color=text_color, x_label=x_label, y_label=y_label)

        # Specific ticks and range in the theta direction
        self.ticks = [(0, '0'), (np.pi/4, 'π/4'), (np.pi/2, 'π/2'), (3*np.pi/4, '3π/4'),
                      (np.pi, 'π'), (5*np.pi/4, '5π/4'), (3*np.pi/2, '3π/2'), (7*np.pi/4, '7π/4'),
                      (2 * np.pi, '2π')]
        self.getAxis('bottom').setTicks([self.ticks, []])
        self.getAxis('top').setTicks([self.ticks, []])
        self.setMouseEnabled(x=False, y=True)
        self.setXRange(0, 2*np.pi)

        # theta
        self.theta = np.linspace(0, 2*np.pi, parameters.theta_res)

        # line 2 (without obstacles)
        self.line2_data = np.ones(parameters.theta_res)
        self.line2 = self.plot(self.theta, self.line2_data, pen=pg.mkPen(self.line2_color, width=2), name="without_obs", antialias=1)

        # line 1 (with obstacles)
        self.line1_data = Math.compute_J_with_obstacles(Math.s, Math.A) / parameters.k
        self.line1 = self.plot(self.theta, self.line1_data, pen=pg.mkPen(self.line1_color, width=2), name="with_obs", antialias=1)

        # filling
        self.fill = pg.FillBetweenItem(self.line1, self.line2, brush=pg.mkBrush((0, 0, 255, 40)))
        self.addItem(self.fill)

    def plot_line1(self):
        Math.s = Math.compute_s(Math.a)
        self.line1_data = Math.compute_J_with_obstacles(Math.s, Math.A) / parameters.k
        self.line1.setData(self.theta, self.line1_data)


class DirectionalityPlot(Custom1DPlot):
    def __init__(self, parent, plot_color, frame_color, line1_color, line2_color, axis_color, ticks_color, text_color, x_label,
                 y_label):
        super().__init__(parent=parent, plot_color=plot_color, frame_color=frame_color, line1_color=line1_color,
                         line2_color=line2_color, axis_color=axis_color, ticks_color=ticks_color,
                         text_color=text_color, x_label=x_label, y_label=y_label)