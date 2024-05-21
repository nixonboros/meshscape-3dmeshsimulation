import numpy as np
import trimesh

def generate_anthill_mesh(radius=1, height=1.5, flat_top_height=1, scale=1.0):
    radius = np.random.uniform(1, 1.5) * scale 
    height = np.random.uniform(1, 1.5)
    flat_top_height = np.random.uniform(1, 1.5) * scale 

    r = np.linspace(0, radius, 100)
    theta = np.linspace(0, 2 * np.pi, 100)
    r, theta = np.meshgrid(r, theta)
    
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    
    z = (height - flat_top_height) * (radius - r) / radius
    z[z < 0] = 0
    z += flat_top_height

    x *= scale
    y *= scale
    z *= scale
    
    vertices = np.vstack((x.flatten(), y.flatten(), z.flatten())).T
    
    # Create faces based on the grid of points
    faces = []
    num_points = x.shape[0] * x.shape[1]
    for i in range(x.shape[0] - 1):
        for j in range(x.shape[1] - 1):
            v0 = i * x.shape[1] + j
            v1 = v0 + 1
            v2 = v0 + x.shape[1]
            v3 = v2 + 1
            faces.append([v0, v1, v2])
            faces.append([v1, v3, v2])
    
    # Convert faces to a numpy array
    faces = np.array(faces)
    
    # Create the mesh
    anthill_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    # Rotate the anthill so Y is up
    anthill_mesh.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(90), [0, 0, 1]
    ))
    
    return anthill_mesh


