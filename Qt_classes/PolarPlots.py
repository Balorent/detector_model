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


class CustomPolarPlot(pg.PlotWidget):
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
        self.getViewBox().setBackgroundColor(self.frame_color)

        # Axis
        for orientation in ["bottom", "right", "top", "left"]:
            self.hideAxis(orientation)


class PolarPlot(CustomPolarPlot):
    def __init__(self, parent, plot_color, frame_color, line1_color, line2_color, axis_color, ticks_color, text_color,
                 x_label, y_label):
        super().__init__(parent=parent, plot_color=plot_color, frame_color=frame_color, line1_color=line1_color,
                         line2_color=line2_color, axis_color=axis_color, ticks_color=ticks_color,
                         text_color=text_color, x_label="", y_label="")

        # Specific ticks and range in the theta direction
        self.ticks = []
        self.getAxis('bottom').setTicks([self.ticks, []])
        self.getAxis('top').setTicks([self.ticks, []])
        self.getAxis('left').setTicks([self.ticks, []])
        self.getAxis('right').setTicks([self.ticks, []])
        # self.setMouseEnabled(x=False, y=False)
        self.setXRange(-4, 4)
        self.setYRange(-4, 4)

        # theta
        self.theta = np.linspace(0, 2*np.pi, parameters.theta_res)
        self.setAspectLocked()

        # Radial grid
        self.circle_zero = 2
        self.circle_max = 5
        self.line_circle_0 = self.plot(self.circle_zero * np.cos(self.theta),
                                       self.circle_zero * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=2),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_1 = self.plot((self.circle_zero+1) * np.cos(self.theta),
                                       (self.circle_zero+1) * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=1),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_2 = self.plot((self.circle_zero+2) * np.cos(self.theta),
                                       (self.circle_zero+2) * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=1),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_3 = self.plot((self.circle_zero+3) * np.cos(self.theta),
                                       (self.circle_zero+3) * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=1),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_4 = self.plot((self.circle_zero+4) * np.cos(self.theta),
                                       (self.circle_zero+4) * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=1),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_5 = self.plot((self.circle_zero+5) * np.cos(self.theta),
                                       (self.circle_zero+5) * np.sin(self.theta),
                                       pen=pg.mkPen("k", width=2),
                                       name="without_obs",
                                       antialias=1)
        self.line_circle_infty = self.plot((self.circle_zero+6) * np.cos(self.theta),
                                           (self.circle_zero+6) * np.sin(self.theta),
                                           pen=pg.mkPen("k", width=1e-10),
                                           name="without_obs",
                                           antialias=1)

        # Angular Grid
        self.angular_ticks = [(0, '0'), (np.pi / 4, 'π/4'), (np.pi / 2, 'π/2'), (3 * np.pi / 4, '3π/4'),
                      (np.pi, 'π'), (5 * np.pi / 4, '5π/4'), (3 * np.pi / 2, '3π/2'), (7 * np.pi / 4, '7π/4')]
        for tick in self.angular_ticks:
            self.addItem(pg.PlotCurveItem(x=[self.circle_zero * np.cos(tick[0]), (self.circle_max + self.circle_zero) * np.cos(tick[0])],
                                          y=[self.circle_zero * np.sin(tick[0]), (self.circle_max + self.circle_zero) * np.sin(tick[0])],
                                          pen=pg.mkPen(self.axis_color, width=0.75),
                                          antialias=1))
            test = pg.TextItem(text=tick[1], color='k')
            self.addItem(test)
            test.setPos((self.circle_zero + self.circle_max)*np.cos(tick[0]), (self.circle_zero + self.circle_max)*np.sin(tick[0]))
            anchor_x = ((np.pi/4 < tick[0] < 3*np.pi/4) or (5*np.pi/4 < tick[0] < 7*np.pi/4))*(np.tan(tick[0]+np.pi/2)+0.5) + (3*np.pi/4 <= tick[0] <= 5*np.pi/4)*1
            anchor_y = ((0 <= tick[0] < np.pi/4) or (3*np.pi/4 < tick[0] < 5*np.pi/4) or (7*np.pi/4 < tick[0] < 2*np.pi))*(np.tan(tick[0])+0.5) + (np.pi/4 <= tick[0] <= 3*np.pi/4)*1
            test.setAnchor((anchor_x, anchor_y))

        # line 2 (without obstacles)
        self.line2_data = np.ones(parameters.theta_res)
        self.line2 = self.plot((self.line2_data+self.circle_zero) * np.cos(self.theta),
                               (self.line2_data+self.circle_zero) * np.sin(self.theta),
                               pen=pg.mkPen(self.line2_color, width=2),
                               name="without_obs",
                               antialias=1)

        # line 1 (with obstacles)
        self.line1_data = Math.compute_J_with_obstacles(Math.s, Math.A) / parameters.k
        r = (self.line1_data<5)*self.line1_data + (self.line1_data>=5)*5 + self.circle_zero
        self.line1 = self.plot(r * np.cos(self.theta),
                               r * np.sin(self.theta),
                               pen=pg.mkPen(self.line1_color, width=2),
                               name="with_obs",
                               antialias=1)

        # filling
        self.fill_white = pg.FillBetweenItem(self.line_circle_0, self.line_circle_5, brush=pg.mkBrush('w'))
        self.addItem(self.fill_white)
        self.fill = pg.FillBetweenItem(self.line1, self.line2, brush=pg.mkBrush((0, 0, 255, 40)))
        self.addItem(self.fill)

    def plot_line1(self):
        Math.s = Math.compute_s(Math.a)
        self.line1_data = Math.compute_J_with_obstacles(Math.s, Math.A) / parameters.k
        r = (self.line1_data < 5) * self.line1_data + (self.line1_data >= 5) * 5 + self.circle_zero
        self.line1.setData(r * np.cos(self.theta),
                           r * np.sin(self.theta))
