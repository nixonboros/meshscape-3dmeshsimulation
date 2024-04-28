import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Parameters for the volcano
radius = 10  # Radius of the base of the cone
height = 15  # Height of the cone
flat_top_height = 10  # Height at which the top becomes flat

# Create a grid of points in polar coordinates
r = np.linspace(0, radius, 100)
theta = np.linspace(0, 2*np.pi, 100)
r, theta = np.meshgrid(r, theta)

# Convert polar coordinates to Cartesian coordinates for the base
x = r * np.cos(theta)
y = r * np.sin(theta)

# Create the height data for the cone
z = (height - flat_top_height) * (radius - r) / radius
z[z < 0] = 0
z += flat_top_height
