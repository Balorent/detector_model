# parameters.py
# --------------------------
# Author : Baptiste Lorent
# latest update : 21/08/2023
# --------------------------

# Import libraries
# Import files

#  Gas parameter
N = 10
radius = 5
coordinates = []

#  Wave parameter
k = 20
wave_type = "sph"  # "sph", or "pl"
plane_wave_angle = 0

#  Model parameters
model = "max"  # "max", or "h-s"
alpha = 1

#  xy plot parameter
scale = "log"  # "log" or "poly" or "step"
x_res = 200
x_min = -10
x_max = 10
y_res = 200
y_min = -10
y_max = 10

#  theta plot parameters
theta_res = 500

#  res_plot parameters
imk_res = 100
imk_min = -2
imk_max = 0
rek_res = 100
rek_min = 0
rek_max = 10

#  Display parameters
scatterers_radius = 0.1
highlight_distance = 0.3

#  Sliders parameters
sliders_clicks = 5000
