import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial import ConvexHull

def rock_generator(num_points):
    # more points mean smoother rocks
    points = np.random.normal(size=(num_points, 3)) 
    # Convex rock shape, so currently not indents or sheer caves etc.
    hull = ConvexHull(points)
    # Point cloud, can just be put into the mesh.
    return(points,hull)

# Currently exports to obj, but can just transfer point cloud to MESH
""" def export_to_obj(rock, filename="rock_shape.obj"):
    points = rock[0]
    hull = rock[1]
    with open(filename, "w") as file:
        for point in points:
            file.write(f"v {point[0]} {point[1]} {point[2]}\n")
        for simplex in hull.simplices:
            face_indices = [str(index + 1) for index in simplex]
            file.write("f " + " ".join(face_indices) + "\n")
            
export_to_obj(rock_generator(10000)) """