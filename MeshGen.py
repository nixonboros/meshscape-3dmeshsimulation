import os
import numpy as np
import collada
import random
import tkinter as tk
from tkinter import ttk

def smooth_elevations(elevations, num_iterations=1):
    for _ in range(num_iterations):
        if not elevations:
            # If elevations is empty, return an empty list
            return []
        smoothed_elevations = [elevations[0]]  # Keep the first endpoint unchanged
        for i in range(1, len(elevations) - 1):
            smoothed_elevation = (elevations[i-1] + 2 * elevations[i] + elevations[i+1]) / 4
            smoothed_elevations.append(smoothed_elevation)
        smoothed_elevations.append(elevations[-1])  # Keep the last endpoint unchanged
        elevations = smoothed_elevations
    return elevations

def generate_dae_mesh(filepath, size_x=50, size_y=50, min_vertices_x=10, max_vertices_x=20, min_vertices_y=10, max_vertices_y=20, box_position=(25, 30, 5)):
    # Convert arguments to integers
    min_vertices_x = int(min_vertices_x)
    max_vertices_x = int(max_vertices_x)
    min_vertices_y = int(min_vertices_y)
    max_vertices_y = int(max_vertices_y)
    
    # Randomly select the number of vertices along x and y directions
    num_vertices_x = random.randint(min_vertices_x, max_vertices_x)
    num_vertices_y = random.randint(min_vertices_y, max_vertices_y)

    # Create a new Collada object
    mesh = collada.Collada()

    # Set the unit meter in the asset
    mesh.assetInfo.unitname = "meter"

    # Create a material for the landscape
    effect_landscape = collada.material.Effect("effect_landscape", [], "phong", diffuse=(0.3, 0.5, 0.3), specular=(0, 0, 0))
    mat_landscape = collada.material.Material("material_landscape", "mymaterial_landscape", effect_landscape)
    mesh.effects.append(effect_landscape)
    mesh.materials.append(mat_landscape)

    # Generate vertices for the flat bottom
    bottom_vertices = []
    for i in range(num_vertices_y):
        for j in range(num_vertices_x):
            x = j * size_x / (num_vertices_x - 1)
            y = i * size_y / (num_vertices_y - 1)
            z = 0  # Bottom starts at z = 0
            bottom_vertices.append((x, y, z))

    # Create vertex source for the bottom
    vert_src_bottom = collada.source.FloatSource("vertices-array-bottom", np.array(bottom_vertices).flatten(), ('X', 'Y', 'Z'))
    geom_bottom = collada.geometry.Geometry(mesh, "geometry_bottom", "bottom_mesh", [vert_src_bottom])

    input_list_bottom = collada.source.InputList()
    input_list_bottom.addInput(0, 'VERTEX', "#vertices-array-bottom")

    # Generate triangles for the bottom
    indices_bottom = []
    for i in range(num_vertices_y - 1):
        for j in range(num_vertices_x - 1):
            v0 = i * num_vertices_x + j
            v1 = v0 + 1
            v2 = (i + 1) * num_vertices_x + j
            v3 = v2 + 1
            indices_bottom.extend([v0, v1, v2, v1, v3, v2])

    # Create triangle set for the bottom
    triset_bottom = geom_bottom.createTriangleSet(np.array(indices_bottom), input_list_bottom, "materialref_bottom")
    geom_bottom.primitives.append(triset_bottom)

    mesh.geometries.append(geom_bottom)

    # Generate landscape vertices on top of the flat bottom
    landscape_vertices = []
    for i in range(num_vertices_y):
        for j in range(num_vertices_x):
            x = j * size_x / (num_vertices_x - 1)
            y = i * size_y / (num_vertices_y - 1)
            # Generate random elevation for the landscape
            z = random.uniform(0, 8)  # Adjust the range as needed
            landscape_vertices.append((x, y, z))

    # Smooth the elevations
    elevations = [vertex[2] for vertex in landscape_vertices]
    smoothed_elevations = smooth_elevations(elevations, num_iterations=3)

    # Update the vertices with smoothed elevations
    for i, vertex in enumerate(landscape_vertices):
        landscape_vertices[i] = (vertex[0], vertex[1], smoothed_elevations[i])

    # Create vertex source for the landscape
    vert_src_landscape = collada.source.FloatSource("vertices-array-landscape", np.array(landscape_vertices).flatten(), ('X', 'Y', 'Z'))
    geom_landscape = collada.geometry.Geometry(mesh, "geometry_landscape", "landscape_mesh", [vert_src_landscape])

    input_list_landscape = collada.source.InputList()
    input_list_landscape.addInput(0, 'VERTEX', "#vertices-array-landscape")

    # Generate triangles for the landscape
    indices_landscape = []
    for i in range(num_vertices_y - 1):
        for j in range(num_vertices_x - 1):
            v0 = i * num_vertices_x + j
            v1 = v0 + 1
            v2 = (i + 1) * num_vertices_x + j
            v3 = v2 + 1
            indices_landscape.extend([v0, v1, v2, v1, v3, v2])

    # Create triangle set for the landscape
    triset_landscape = geom_landscape.createTriangleSet(np.array(indices_landscape), input_list_landscape, "materialref_landscape")
    geom_landscape.primitives.append(triset_landscape)

    mesh.geometries.append(geom_landscape)

    # Generate box geometry with specified position
    vertices_box = np.array([
        [box_position[0], box_position[1], box_position[2]],  # Front bottom left
        [box_position[0] + 1, box_position[1], box_position[2]],  # Front bottom right
        [box_position[0] + 1, box_position[1] + 0.5, box_position[2]],  # Front top right
        [box_position[0], box_position[1] + 0.5, box_position[2]],  # Front top left
        [box_position[0], box_position[1], box_position[2] + 0.5],  # Back bottom left
        [box_position[0] + 1, box_position[1], box_position[2] + 0.5],  # Back bottom right
        [box_position[0] + 1, box_position[1] + 0.5, box_position[2] + 0.5],  # Back top right
        [box_position[0], box_position[1] + 0.5, box_position[2] + 0.5],  # Back top left
    ])

    indices_box = np.array([
        0, 1, 2, 0, 2, 3,  # Front face
        4, 5, 6, 4, 6, 7,  # Back face
        0, 4, 5, 0, 5, 1,  # Left side
        1, 5, 6, 1, 6, 2,  # Top side
        2, 6, 7, 2, 7, 3,  # Right side
        3, 7, 4, 3, 4, 0,  # Bottom side
    ])

    # Create vertex source for the box
    vert_src_box = collada.source.FloatSource("vertices-array-box", vertices_box.flatten(), ('X', 'Y', 'Z'))
    geom_box = collada.geometry.Geometry(mesh, "geometry_box", "box_mesh", [vert_src_box])

    input_list_box = collada.source.InputList()
    input_list_box.addInput(0, 'VERTEX', "#vertices-array-box")

    # Create triangle set for the box
    triset_box = geom_box.createTriangleSet(indices_box, input_list_box, "materialref_box")
    geom_box.primitives.append(triset_box)

    mesh.geometries.append(geom_box)

    # Create a tree geometry
    tree_vertices = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0],
        [0, 1, 0],
        [0, 0, 1],
        [1, 0, 1],
        [1, 1, 1],
        [0, 1, 1]
    ])
    tree_indices = np.array([
        0, 1, 2, 0, 2, 3,
        4, 5, 6, 4, 6, 7,
        0, 4, 5, 0, 5, 1,
        1, 5, 6, 1, 6, 2,
        2, 6, 7, 2, 7, 3,
        3, 7, 4, 3, 4, 0
    ])

    # Create vertex source for the tree
    vert_src_tree = collada.source.FloatSource("vertices-array-tree", tree_vertices.flatten(), ('X', 'Y', 'Z'))
    geom_tree = collada.geometry.Geometry(mesh, "geometry_tree", "tree_mesh", [vert_src_tree])

    input_list_tree = collada.source.InputList()
    input_list_tree.addInput(0, 'VERTEX', "#vertices-array-tree")

    # Create triangle set for the tree
    triset_tree = geom_tree.createTriangleSet(tree_indices, input_list_tree, "materialref_tree")
    geom_tree.primitives.append(triset_tree)

    mesh.geometries.append(geom_tree)

    # Create a material for the tree
    effect_tree = collada.material.Effect("effect_tree", [], "phong", diffuse=(0.3, 0.5, 0.3), specular=(0, 0, 0))
    mat_tree = collada.material.Material("material_tree", "mymaterial_tree", effect_tree)
    mesh.effects.append(effect_tree)
    mesh.materials.append(mat_tree)

    # Specify tree positions
    tree_positions = [(10, 10, 0), (15, 20, 1), (30, 25, 2)]  # Adjust positions as needed

    # Create a scene
    geomnode_bottom = collada.scene.GeometryNode(geom_bottom, [mat_landscape])
    geomnode_landscape = collada.scene.GeometryNode(geom_landscape, [mat_landscape])
    geomnode_box = collada.scene.GeometryNode(geom_box, [mat_landscape])
    node_bottom = collada.scene.Node("node_bottom", children=[geomnode_bottom])
    node_landscape = collada.scene.Node("node_landscape", children=[geomnode_landscape])
    node_box = collada.scene.Node("node_box", children=[geomnode_box])

    myscene = collada.scene.Scene("myscene", [node_bottom, node_landscape, node_box])

    # Add tree nodes to the scene
    for tree_position in tree_positions:
        # Create a geometry node for the tree
        geomnode_tree = collada.scene.GeometryNode(geom_tree, [mat_tree])

        # Create a node for the tree with its position
        tree_node = collada.scene.Node("tree_node", children=[geomnode_tree])
        tree_node.translation = tree_position  # Set the position of the tree

        # Add the tree node to the scene
        myscene.nodes.append(tree_node)

    mesh.scenes.append(myscene)
    mesh.scene = myscene

    # Save to file
    mesh.write(filepath)

def generate_mesh(_=None):
    # Specify the subfolder name
    subfolder_name = "GeneratedMeshes"
    # Get the current working directory
    cwd = os.getcwd()
    # Create the full path for the subfolder
    subfolder_path = os.path.join(cwd, subfolder_name)
    # Create the subfolder if it doesn't exist
    os.makedirs(subfolder_path, exist_ok=True)
    # Specify the output file name within the subfolder
    output_file_path = os.path.join(subfolder_path, "landscape_from_gui.dae")
    # Generate the mesh using the specified output file path and slider values
    generate_dae_mesh(output_file_path, 
                      size_x=size_x_scale.get(), 
                      size_y=size_y_scale.get(),
                      min_vertices_x=min_vertices_x_scale.get(),
                      max_vertices_x=max_vertices_x_scale.get(),
                      min_vertices_y=min_vertices_y_scale.get(),
                      max_vertices_y=max_vertices_y_scale.get())

def update_slider_labels():
    size_x_label.config(text=f"Size X: {size_x_scale.get():.2f}")
    size_y_label.config(text=f"Size Y: {size_y_scale.get():.2f}")
    min_vertices_x_label.config(text=f"Min Vertices X: {min_vertices_x_scale.get():.2f}")
    max_vertices_x_label.config(text=f"Max Vertices X: {max_vertices_x_scale.get():.2f}")
    min_vertices_y_label.config(text=f"Min Vertices Y: {min_vertices_y_scale.get():.2f}")
    max_vertices_y_label.config(text=f"Max Vertices Y: {max_vertices_y_scale.get():.2f}")


def update_min_slider(max_slider_value, min_slider_scale):
    # Update the minimum slider's range based on the maximum slider value
    min_slider_scale.configure(to=max_slider_value)
    update_slider_labels()

# GUI setup
window = tk.Tk()
window.title("Mesh Generator")

# Slider for size along X
size_x_scale = ttk.Scale(window, from_=10, to=100, length=200, orient="horizontal", value=10)
size_x_scale.grid(row=0, column=0, padx=10, pady=10)
size_x_label = ttk.Label(window, text=f"Size X: {size_x_scale.get():.2f}")
size_x_label.grid(row=0, column=1)

# Slider for size along Y
size_y_scale = ttk.Scale(window, from_=10, to=100, length=200, orient="horizontal", value=10)
size_y_scale.grid(row=1, column=0, padx=10, pady=10)
size_y_label = ttk.Label(window, text=f"Size Y: {size_y_scale.get():.2f}")
size_y_label.grid(row=1, column=1)

# Slider for min vertices along X
min_vertices_x_scale = ttk.Scale(window, from_=5, to=20, length=200, orient="horizontal", value=5)
min_vertices_x_scale.grid(row=2, column=0, padx=10, pady=10)
min_vertices_x_label = ttk.Label(window, text=f"Min Vertices X: {min_vertices_x_scale.get():.2f}")
min_vertices_x_label.grid(row=2, column=1)

# Slider for max vertices along X
max_vertices_x_scale = ttk.Scale(window, from_=10, to=30, length=200, orient="horizontal", value=10)
max_vertices_x_scale.grid(row=3, column=0, padx=10, pady=10)
max_vertices_x_label = ttk.Label(window, text=f"Max Vertices X: {max_vertices_x_scale.get():.2f}")
max_vertices_x_label.grid(row=3, column=1)

# Slider for min vertices along Y
min_vertices_y_scale = ttk.Scale(window, from_=5, to=20, length=200, orient="horizontal", value=5)
min_vertices_y_scale.grid(row=4, column=0, padx=10, pady=10)
min_vertices_y_label = ttk.Label(window, text=f"Min Vertices Y: {min_vertices_y_scale.get():.2f}")
min_vertices_y_label.grid(row=4, column=1)

# Slider for max vertices along Y
max_vertices_y_scale = ttk.Scale(window, from_=10, to=30, length=200, orient="horizontal", value=10)
max_vertices_y_scale.grid(row=5, column=0, padx=10, pady=10)
max_vertices_y_label = ttk.Label(window, text=f"Max Vertices Y: {max_vertices_y_scale.get():.2f}")
max_vertices_y_label.grid(row=5, column=1)

generate_button = ttk.Button(window, text="Generate Mesh", command=generate_mesh)
generate_button.grid(row=8, column=1)  # Adjust row and column as needed

update_slider_labels()  # Update labels with initial values

# Continuous update of slider labels
size_x_scale.bind("<ButtonRelease-1>", lambda event: update_slider_labels())
size_y_scale.bind("<ButtonRelease-1>", lambda event: update_slider_labels())
min_vertices_x_scale.bind("<ButtonRelease-1>", lambda event: update_slider_labels())
max_vertices_x_scale.bind("<ButtonRelease-1>", lambda event: [update_slider_labels(), update_min_slider(max_vertices_x_scale.get(), min_vertices_x_scale)])
min_vertices_y_scale.bind("<ButtonRelease-1>", lambda event: update_slider_labels())
max_vertices_y_scale.bind("<ButtonRelease-1>", lambda event: [update_slider_labels(), update_min_slider(max_vertices_y_scale.get(), min_vertices_y_scale)])

window.mainloop()



#add slider for vertice height
#add slider for smoothness
#fix adding objects e.g. trees