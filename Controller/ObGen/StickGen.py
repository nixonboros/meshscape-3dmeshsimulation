import numpy as np
import trimesh
import random

def stick_mesh(base_position, height, thickness):
    x, y, z = base_position
    
    # Define the vertices of the stick
    vertices = np.array([
        [x - thickness, y - thickness, z],
        [x + thickness, y - thickness, z],
        [x + thickness, y + thickness, z],
        [x - thickness, y + thickness, z],
        [x - thickness, y - thickness, z + height],
        [x + thickness, y - thickness, z + height],
        [x + thickness, y + thickness, z + height],
        [x - thickness, y + thickness, z + height]
    ])
    
    # Define the faces of the stick
    faces = np.array([
        [0, 1, 2], [0, 2, 3],
        [4, 5, 6], [4, 6, 7],
        [0, 1, 5], [0, 5, 4],
        [1, 2, 6], [1, 6, 5],
        [2, 3, 7], [2, 7, 6],
        [3, 0, 4], [3, 4, 7]
    ])
    
    # Create the mesh
    stick_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    return stick_mesh

# Parameters
height = random.uniform(1, 5)  # Random stick height between 1 and 5 units
thickness = random.uniform(0.05, 0.2)  # Random stick thickness
size_x, size_y = 10, 10
base_position = (random.uniform(0, size_x), random.uniform(0, size_y), random.uniform(0, 5))  # Random base position

# Generate the stick mesh
stick = stick_mesh(base_position, height, thickness)

# Show the stick mesh
stick.show()
