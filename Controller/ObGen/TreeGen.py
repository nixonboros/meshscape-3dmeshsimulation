import numpy as np
import trimesh

def generate_cylinder(radius, height, divisions=20, scale=1.0):
    vertices = []
    faces = []
    radius_scaled = radius * scale
    height_scaled = height * scale
    for i in range(divisions):
        angle = 2 * np.pi * i / divisions
        x = radius_scaled * np.cos(angle)
        y = radius_scaled * np.sin(angle)
        vertices.append((x, y, 0))  # Bottom circle
        vertices.append((x, y, height_scaled))  # Top circle
    for i in range(divisions):
        next_index = (i + 1) % divisions
        faces.append((2 * i, 2 * next_index, 2 * next_index + 1))
        faces.append((2 * i, 2 * next_index + 1, 2 * i + 1))
    return vertices, faces

def generate_cone(radius, height, divisions=20, scale=1.0):
    vertices = [(0, 0, height * scale)]  # Tip of the cone
    for i in range(divisions):
        angle = 2 * np.pi * i / divisions
        x = radius * scale * np.cos(angle)
        y = radius * scale * np.sin(angle)
        vertices.append((x, y, 0))  # Base of the cone
    faces = [(0, i + 1, (i + 1) % divisions + 1) for i in range(divisions)]
    return vertices, faces

def generate_tree(scale=0.1):
    trunk_height = np.random.uniform(5.0, 10.0)
    trunk_radius = np.random.uniform(1, 3)
    crown_height = np.random.uniform(15.0, 30.0)
    crown_radius = np.random.uniform(5, 10.0)
    trunk_vertices, trunk_faces = generate_cylinder(trunk_radius, trunk_height, 20, scale)
    crown_vertices, crown_faces = generate_cone(crown_radius, crown_height, 20, scale)
    crown_vertices = [(x, y, z + trunk_height * scale) for x, y, z in crown_vertices]
    vertices = trunk_vertices + crown_vertices
    offset = len(trunk_vertices)
    faces = trunk_faces + [[i + offset for i in face] for face in crown_faces]
    return vertices, faces


# Convert tree data to a Trimesh object (to integrate with other parts)
def tree_to_trimesh(vertices, faces):
    return trimesh.Trimesh(vertices=vertices, faces=faces)
