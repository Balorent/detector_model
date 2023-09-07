# Import libraries
import numpy as np
# Import files
import parameters
import Math


def add_random(root, N):
    radius = parameters.radius
    for i in range(N):
        x = np.random.random()*2*radius - radius
        y = np.random.random()*2*radius - radius
        while np.sqrt(x * x + y * y) > radius:
            x = np.random.random()*2*radius - radius
            y = np.random.random()*2*radius - radius
        parameters.coordinates.append([x, y])
        parameters.N += 1
        root.XY_frame.graph.scatterers.add_scatterer()
        root.XY_frame.graph.plot_2d(update=True, autoRange=False, autoLevels=False)
        root.Theta_frame.graph.plot_line1()


def remove_all(root):
    parameters.coordinates = []
    parameters.N = 0
    root.XY_frame.graph.scatterers.remove_all_scatterers()
    root.XY_frame.graph.plot_2d(update=True, autoRange=False, autoLevels=False)
    root.Theta_frame.graph.plot_line1()
