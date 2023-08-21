# initialize.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
import numpy as np
# Import files
import parameters


def init_scatterers():
    N = parameters.N
    x_min = parameters.x_min
    x_max = parameters.x_max
    y_min = parameters.y_min
    y_max = parameters.y_max
    radius = parameters.radius
    for i in range(N):
        x = np.random.random() * (x_max - x_min) + x_min
        y = np.random.random() * (y_max - y_min) + y_min
        while np.sqrt(x*x + y*y) > radius:
            x = np.random.random() * (x_max - x_min) + x_min
            y = np.random.random() * (y_max - y_min) + y_min
        parameters.coordinates.append((x, y))
