import numpy as np
import trimesh
import random

def create_leaf(scale):
    # leaf
    leaf_scale = random.uniform(0.05, 0.08) * scale
    leaf_shape = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0.5, 1, 0]
    ]) * leaf_scale
    
    leaf_faces = np.array([
        [0, 1, 2]
    ])
    
    leaf = trimesh.Trimesh(vertices=leaf_shape, faces=leaf_faces)
    return leaf

def create_stick(scale):
    # sticks
    radius = random.uniform(0.01, 0.02) * scale
    height = random.uniform(0.1, 0.2) * scale
    stick = trimesh.creation.cylinder(radius, height, sections=10)
    return stick

def create_bit(scale):
    # cubes and spheres
    if np.random.rand() > 0.5:
        size = random.uniform(0.001, 0.0015) * scale
        bit = trimesh.creation.box(extents=[size, size, size])
    else:
        radius = random.uniform(0.005, 0.0075) * scale
        bit = trimesh.creation.icosphere(radius=radius)
    return bit

def create_bush(num_leaves=800, num_sticks=15, num_bits=50, scale=1.0):
    all_vertices = []
    all_faces = []
    face_offset = 0

    for _ in range(num_leaves):
        leaf = create_leaf(scale)
        translation = (np.random.rand(3) - 0.5) * 0.1 * scale
        rotation = trimesh.transformations.random_rotation_matrix()
        leaf.apply_translation(translation)
        leaf.apply_transform(rotation)
        all_vertices.append(leaf.vertices)
        all_faces.append(leaf.faces + face_offset)
        face_offset += len(leaf.vertices)
    
    for _ in range(num_sticks):
        stick = create_stick(scale)
        translation = (np.random.rand(3) - 0.5) * 0.1 * scale
        rotation = trimesh.transformations.random_rotation_matrix()
        stick.apply_translation(translation)
        stick.apply_transform(rotation)
        all_vertices.append(stick.vertices)
        all_faces.append(stick.faces + face_offset)
        face_offset += len(stick.vertices)
    
    for _ in range(num_bits):
        bit = create_bit(scale)
        translation = (np.random.rand(3) - 0.5) * 0.1 * scale
        rotation = trimesh.transformations.random_rotation_matrix()
        bit.apply_translation(translation)
        bit.apply_transform(rotation)
        all_vertices.append(bit.vertices)
        all_faces.append(bit.faces + face_offset)
        face_offset += len(bit.vertices)
    
    vertices = np.vstack(all_vertices)
    faces = np.vstack(all_faces)
    
    bush_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    return bush_mesh

