import numpy as np
import trimesh
import random

def generate_random_rotation_matrix():
    angle_x = np.deg2rad(random.uniform(0, 360))
    angle_y = np.deg2rad(random.uniform(0, 360))
    angle_z = np.deg2rad(random.uniform(0, 360))

    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])

    Ry = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])

    Rz = np.array([
        [np.cos(angle_z), -np.sin(angle_z), 0],
        [np.sin(angle_z), np.cos(angle_z), 0],
        [0, 0, 1]
    ])

    return Rz @ Ry @ Rx

def generate_wiggly_stick(base_position, length=5, radius=0.1, num_segments=50, perturbation_strength=0.1, scale=1.0):
    # Scale length, radius, and perturbation_strength
    length *= scale
    radius *= scale
    perturbation_strength *= scale

    # Create a basic cylinder
    cylinder = trimesh.creation.cylinder(radius=radius, height=length, sections=num_segments)

    # Apply random perturbations to vertices to make it wiggly
    vertices = cylinder.vertices.copy()
    z_values = np.unique(vertices[:, 2])
    for z in z_values:
        mask = (vertices[:, 2] == z)
        perturbation = np.random.normal(0, perturbation_strength, size=(mask.sum(), 2))
        vertices[mask, :2] += perturbation

    # Apply random rotation
    rotation_matrix = generate_random_rotation_matrix()
    vertices = vertices @ rotation_matrix.T

    # Translate to base position
    vertices += np.array(base_position)

    # Create the mesh with modified vertices
    wiggly_stick_mesh = trimesh.Trimesh(vertices=vertices, faces=cylinder.faces)
    return wiggly_stick_mesh

def add_protrusions(mesh, num_protrusions=5, protrusion_length=1, protrusion_radius=0.05, scale=1.0):
    combined_mesh = mesh.copy()
    z_range = mesh.bounds[1][2] - mesh.bounds[0][2]

    for _ in range(num_protrusions):
        # Randomly choose a point along the main cylinder
        z_position = random.uniform(0, z_range)
        mask = np.isclose(mesh.vertices[:, 2], z_position, atol=0.1)
        candidate_vertices = mesh.vertices[mask]

        if len(candidate_vertices) == 0:
            continue

        base_vertex = candidate_vertices[random.randint(0, len(candidate_vertices) - 1)]

        # Create a small wiggly stick as a protrusion
        protrusion_base = base_vertex
        protrusion = generate_wiggly_stick(protrusion_base, length=protrusion_length * scale, radius=protrusion_radius * scale, scale=scale)

        # Combine with the main mesh
        combined_mesh = trimesh.util.concatenate([combined_mesh, protrusion])

    return combined_mesh

base_position = (0, 0, 0)

scale_factor = 0.5  
main_stick_mesh = generate_wiggly_stick(base_position, scale=scale_factor)

stick_with_protrusions = add_protrusions(main_stick_mesh, num_protrusions=5, protrusion_length=1, protrusion_radius=0.05, scale=scale_factor)


