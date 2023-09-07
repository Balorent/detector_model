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
    radius = parameters.radius
    for i in range(N):
        x = np.random.random()*2*radius - radius
        y = np.random.random()*2*radius - radius
        while np.sqrt(x*x + y*y) > radius:
            x = np.random.random()*2*radius - radius
            y = np.random.random()*2*radius - radius
        parameters.coordinates.append((x, y))
