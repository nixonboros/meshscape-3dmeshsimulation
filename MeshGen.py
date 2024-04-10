import os
import numpy as np
import collada
import random
import tkinter as tk
from tkinter import ttk

def generate_log(mesh, base_position, height, thickness):
    x, y, z = base_position
    # Introducing slight variability in log ends for a more natural look
    top_thickness = thickness * random.uniform(0.9, 1.1)
    bottom_thickness = thickness * random.uniform(0.9, 1.1)
    
    vertices = np.array([
        [x - bottom_thickness, y - bottom_thickness, z],
        [x + bottom_thickness, y - bottom_thickness, z],
        [x + bottom_thickness, y + bottom_thickness, z],
        [x - bottom_thickness, y + bottom_thickness, z],
        [x - top_thickness, y - top_thickness, z + height],
        [x + top_thickness, y - top_thickness, z + height],
        [x + top_thickness, y + top_thickness, z + height],
        [x - top_thickness, y + top_thickness, z + height]
    ])
    indices = np.array([
        0, 1, 2, 0, 2, 3,  # Bottom face
        4, 5, 6, 4, 6, 7,  # Top face
        0, 4, 5, 0, 5, 1,  # Sides
        1, 5, 6, 1, 6, 2,
        2, 6, 7, 2, 7, 3,
        3, 7, 4, 3, 4, 0
    ])
    vert_src = collada.source.FloatSource(f"log_vertices_{random.random()}", vertices.flatten(), ('X', 'Y', 'Z'))
    geom = collada.geometry.Geometry(mesh, f"log_geometry_{random.random()}", "log_mesh", [vert_src])
    input_list = collada.source.InputList()
    input_list.addInput(0, 'VERTEX', f"#{vert_src.id}")
    triset = geom.createTriangleSet(indices, input_list, "materialref_log")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)
    geom_node = collada.scene.GeometryNode(geom, [])
    node = collada.scene.Node(f"log_node_{random.random()}", children=[geom_node])
    return node

# Initialize a COLLADA document
dae = collada.Collada()

# Define parameters
num_logs = 5
size_x = 100
size_y = 100

# Example loop for generating and adding logs
for _ in range(num_logs):
    height = random.uniform(3, 10)
    thickness = random.uniform(0.5, 1.5)
    base_position = (random.uniform(0, size_x), random.uniform(0, size_y), random.uniform(0, 5))
    generate_log(dae, base_position, height, thickness)

# After generating all logs, save the COLLADA document
dae.write('C:\\test\\my_model.dae')
