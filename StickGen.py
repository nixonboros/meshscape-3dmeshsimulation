import os
import numpy as np
import collada
import random
import tkinter as tk
from tkinter import ttk

def generate_stick(mesh, base_position, height, thickness):
    x, y, z = base_position
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
    indices = np.array([
        0, 1, 2, 0, 2, 3,
        4, 5, 6, 4, 6, 7,
        0, 4, 5, 0, 5, 1,
        1, 5, 6, 1, 6, 2,
        2, 6, 7, 2, 7, 3,
        3, 7, 4, 3, 4, 0
    ])
    vert_src = collada.source.FloatSource(f"stick_vertices_{random.random()}", vertices.flatten(), ('X', 'Y', 'Z'))
    geom = collada.geometry.Geometry(mesh, f"stick_geometry_{random.random()}", "stick_mesh", [vert_src])
    input_list = collada.source.InputList()
    input_list.addInput(0, 'VERTEX', f"#{vert_src.id}")
    triset = geom.createTriangleSet(indices, input_list, "materialref_stick")
    geom.primitives.append(triset)
    mesh.geometries.append(geom)
    geom_node = collada.scene.GeometryNode(geom, [])
    node = collada.scene.Node(f"stick_node_{random.random()}", children=[geom_node])
    return node
    
for _ in range(num_sticks):
    height = random.uniform(1, 5)  # Random stick height between 1 and 5 units
    thickness = random.uniform(0.05, 0.2)  # Random stick thickness
    base_position = (random.uniform(0, size_x), random.uniform(0, size_y), random.uniform(0, 5))  # Random base position
    stick_node = generate_stick(mesh, base_position, height, thickness)
    myscene.nodes.append(stick_node)     