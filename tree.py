import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def random_tree():
    # set minimum and maximum values for size of tree
    trunk_height = np.random.uniform(2,4)
    trunk_radius = np.random.uniform(0.1, 0.2)
    
    # Creating branches
    branch_height = np.random.uniform(trunk_height + 1, trunk_height + 3)
    branch_base = np.random.uniform(trunk_radius + 0.2, trunk_radius + 0.5)
    branch_points = []
    branch_angle = np.linspace(0, 2*np.pi)
    for z in np.linspace(trunk_height, trunk_height + branch_height):
        for angle in branch_angle:
            radius = branch_base * (1 - z / (trunk_height + branch_height))
            x = radius * np.cos(angle)
            y = radius * np.sin(angle)
            branch_points.append([x, y, z])

    # Creating tree trunk
    points = []
    resolution = 100
    tree_angle = np.linspace(0, 2*np.pi, resolution)
    for z in np.linspace(0, trunk_height, resolution):
        for angle in tree_angle:
            x = trunk_radius * np.cos(angle)
            y = trunk_radius * np.sin(angle)
            points.append([x, y, z])
    
    
    # Connect the trunk and the branch
    tree = np.concatenate([branch_points, points], axis=0)
    
    return tree
