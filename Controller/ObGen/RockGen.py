import numpy as np
from scipy.spatial import ConvexHull
from stl import mesh

def rock_generator(num_points, scale_min=0.1, scale_max=0.2):
    # Generate random points
    points = np.random.normal(size=(num_points, 3))
    
    # Apply random scale between scale_min and scale_max
    scale = np.random.uniform(scale_min, scale_max)
    points *= scale
    
    # Create a convex hull
    hull = ConvexHull(points)
    return points, hull

def export_to_stl(points, hull, filename="rock_shape.stl", scale=1.0):
    # Scale points before creating the mesh
    points = points * scale

    # Create an empty mesh
    rock_mesh = mesh.Mesh(np.zeros(hull.simplices.shape[0], dtype=mesh.Mesh.dtype))

    # Loop through the triangles defined by the simplices
    for i, f in enumerate(hull.simplices):
        for j in range(3):
            # Assign the scaled vertex coordinates to the mesh
            rock_mesh.vectors[i][j] = points[f[j], :]

    # Save the mesh to file
    rock_mesh.save(filename)
