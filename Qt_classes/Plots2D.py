# Plots2D.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
import pyqtgraph as pg
import numpy as np
# Import files
import parameters


class Custom2DPlot(pg.PlotItem):
    def __init__(self, plot_color, frame_color, axis_color, ticks_color, text_color, x_label, y_label, x_min, x_max, x_res,
                 y_min, y_max, y_res):
        super().__init__()

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

        # Data
        self.data = np.log(1/np.sqrt(self.mesh[0]**2 + self.mesh[1]**2))
        self.image_view.setImage(self.data,
                                 pos=(self.x_min, self.y_min),
                                 scale=((self.x_max - self.x_min) / self.x_res, (self.y_max - self.y_min) / self.y_res),
                                 autoRange=False)

        # Connect signals
        self.getViewBox().sigRangeChanged.connect(self.range_changed)

    def range_changed(self, event):
        self.view_range = self.getViewBox().viewRange()
        self.x_min, self.x_max = self.view_range[0][0], self.view_range[0][1]
        self.y_min, self.y_max = self.view_range[1][0], self.view_range[1][1]
        self.mesh = np.meshgrid(np.linspace(self.y_min, self.y_max, self.y_res),
                                np.linspace(self.x_min, self.x_max, self.x_res))
        self.data = np.log(1/np.sqrt(self.mesh[0]**2 + self.mesh[1]**2))
        self.image_view.setImage(self.data,
                                 pos=(self.x_min, self.y_min),
                                 scale=((self.x_max - self.x_min) / self.x_res, (self.y_max - self.y_min) / self.y_res),
                                 autoRange=False, autoLevels=False)


class XYPlot(Custom2DPlot):
    def __init__(self, plot_color, frame_color, axis_color, ticks_color, text_color, x_label, y_label):
        super().__init__(plot_color=plot_color, frame_color=frame_color, axis_color=axis_color, ticks_color=ticks_color,
                         text_color=text_color, x_label=x_label, y_label=y_label, x_min=parameters.x_min,
                         x_max=parameters.x_max, x_res=parameters.x_res, y_min=parameters.y_min, y_max=parameters.y_max,
                         y_res=parameters.y_res)
