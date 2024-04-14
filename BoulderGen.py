import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

def boulder_generator(num_points, scale):
    # more points mean smoother rocks
    points = np.random.normal(size=(num_points, 3)) * scale
    # Convex rock shape, so currently not indents or sheer caves etc.
    hull = ConvexHull(points)
    # Point cloud, can just be put into the mesh.
    return(points,hull)

num_points = 400  # number of points in the rock
scale = 20  # increase size to create a larger boulder
points, hull = boulder_generator(num_points, scale)
