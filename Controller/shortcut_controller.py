# Import libraries
import numpy as np
# Import files
import parameters
import Math


def remove_selected(root):
    selected = root.XY_frame.graph.scatterers.state == 2
    if np.any(selected):
        index = int(np.where(selected)[0])
        parameters.coordinates.pop(index)
        parameters.N -= 1
        root.XY_frame.graph.scatterers.remove_scatterer(index)
        root.XY_frame.graph.plot_2d(update=True, autoRange=False, autoLevels=False)
        root.Theta_frame.graph.plot_line1()
