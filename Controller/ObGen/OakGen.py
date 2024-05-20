import numpy as np
import trimesh

def mushroom_mesh(scale=1.0):

    radius = np.random.uniform(1, 1.5) * scale  # Radius of the mushroom cap
    num_petal_points = np.random.randint(30, 60)  # Number of points for the petal
    stem_height = np.random.uniform(2, 3) * scale  # Height of the stem
    stem_radius = np.random.uniform(0.2, 0.3) * scale  # Radius of the stem
    
    # Generate petal coordinates
    theta = np.linspace(0, np.pi, num_petal_points)
    phi = np.linspace(0, 2 * np.pi, num_petal_points)
    theta, phi = np.meshgrid(theta, phi)
    
    x_petal = radius * np.sin(theta) * np.cos(phi)
    z_petal = radius * np.sin(theta) * np.sin(phi)
    y_petal = (radius * np.cos(theta)) + stem_height
    
    # Generate stem coordinates
    stem_theta = np.linspace(0, 2 * np.pi, num_petal_points)
    stem_y = np.linspace(0, stem_height, num_petal_points)
    stem_theta, stem_y = np.meshgrid(stem_theta, stem_y)
    
    x_stem = stem_radius * np.cos(stem_theta)
    z_stem = stem_radius * np.sin(stem_theta)
    y_stem = stem_y
    
    # Combine the petal and stem coordinates into a single set of vertices and faces
    petal_vertices = np.column_stack((x_petal.ravel(), y_petal.ravel(), z_petal.ravel()))
    stem_vertices = np.column_stack((x_stem.ravel(), y_stem.ravel(), z_stem.ravel()))
    
    vertices = np.vstack((petal_vertices, stem_vertices))
    
    # Generate faces for the petal
    petal_faces = []
    for i in range(num_petal_points - 1):
        for j in range(num_petal_points - 1):
            petal_faces.append([i * num_petal_points + j,
                                i * num_petal_points + (j + 1),
                                (i + 1) * num_petal_points + j])
            petal_faces.append([(i + 1) * num_petal_points + j,
                                i * num_petal_points + (j + 1),
                                (i + 1) * num_petal_points + (j + 1)])
    
    # Generate faces for the stem
    stem_faces = []
    offset = len(petal_vertices)
    for i in range(num_petal_points - 1):
        for j in range(num_petal_points - 1):
            stem_faces.append([offset + i * num_petal_points + j,
                               offset + i * num_petal_points + (j + 1),
                               offset + (i + 1) * num_petal_points + j])
            stem_faces.append([offset + (i + 1) * num_petal_points + j,
                               offset + i * num_petal_points + (j + 1),
                               offset + (i + 1) * num_petal_points + (j + 1)])
    
    faces = np.vstack((petal_faces, stem_faces))
    
    # Create the mesh
    mushroom_mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    
    # Rotate the mushroom so Y is up
    mushroom_mesh.apply_transform(trimesh.transformations.rotation_matrix(
        np.radians(90), [1, 0, 0]
    ))
    
    return mushroom_mesh


