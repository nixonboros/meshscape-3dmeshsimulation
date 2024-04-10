import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Function to generate coordinates for a mushroom mesh
def mushroom_mesh(radius=1, petal_width=0.2, num_petal_points=50, stem_height=2, stem_radius=0.1):
    
    theta = np.linspace(0, np.pi, num_petal_points)
    phi = np.linspace(0, 2*np.pi, num_petal_points)
    theta, phi = np.meshgrid(theta, phi)
    
    mushroom_x_petal = radius * np.sin(theta) * np.cos(phi)
    mushroom_y_petal = radius * np.sin(theta) * np.sin(phi)
    mushroom_z_petal = (radius * np.cos(theta)) + stem_height
    
    mushroom_stem_theta = np.linspace(0, 2*np.pi, num_petal_points)
    mushroom_stem_z = np.linspace(0, stem_height, num_petal_points)
    mushroom_stem_theta, stem_z = np.meshgrid(stem_theta, stem_z)
    
    mushroom_stem_x = stem_radius * np.cos(stem_theta)
    mushroom_stem_y = stem_radius * np.sin(stem_theta)
    mushroom_stem_z = stem_z
    
    return x_petal, y_petal, z_petal, stem_x, stem_y, stem_z

