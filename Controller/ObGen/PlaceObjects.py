import numpy as np
import trimesh
import tkinter as tk
from tkinter import filedialog

from .OakGen import mushroom_mesh
from .TreeGen import generate_tree, tree_to_trimesh
from .RockGen import rock_generator
from .AntHillGen import generate_anthill_mesh
from .StickGen import generate_wiggly_stick
from .BushGen import create_bush

def place_objects_on_terrain(terrain_path, num_rocks=5, points_per_rock=1000, rock_scale_min=0.05, rock_scale_max=0.1, num_trees=5, tree_scale=0.1, num_mushrooms=5, mushroom_scale=0.1, num_anthills=3, anthill_scale=1.0, num_sticks=10, stick_scale=0.5, num_bushes=10, bushes_scale=0.2):
    # Load the terrain STL file
    terrain = trimesh.load(terrain_path)

    # Get terrain bounds for positioning
    min_x, min_y, _ = terrain.bounds[0]
    max_x, max_y, _ = terrain.bounds[1]

    objects = []

    # Place rocks
    for _ in range(num_rocks):
        points, hull = rock_generator(points_per_rock, rock_scale_min, rock_scale_max)
        rock_mesh = trimesh.Trimesh(vertices=points, faces=hull.simplices)
        rock_mesh = position_object_on_terrain(rock_mesh, terrain, min_x, max_x, min_y, max_y)
        objects.append(rock_mesh)

    # Place trees
    for _ in range(num_trees):
        vertices, faces = generate_tree(tree_scale)
        tree_mesh = tree_to_trimesh(vertices, faces)
        tree_mesh = position_object_on_terrain(tree_mesh, terrain, min_x, max_x, min_y, max_y)
        objects.append(tree_mesh)

    # Place mushrooms
    for _ in range(num_mushrooms):
        mushroom = mushroom_mesh(mushroom_scale)
        mushroom_mesh_pos = position_object_on_terrain(mushroom, terrain, min_x, max_x, min_y, max_y)
        objects.append(mushroom_mesh_pos)

    # Place anthills
    for _ in range(num_anthills):
        anthill = generate_anthill_mesh(scale=anthill_scale)
        anthill_mesh_pos = position_object_on_terrain(anthill, terrain, min_x, max_x, min_y, max_y)
        objects.append(anthill_mesh_pos)

    # Place sticks
    for _ in range(num_sticks):
        stick = generate_wiggly_stick([0, 0, 0], scale=stick_scale)
        stick_mesh_pos = position_object_on_terrain(stick, terrain, min_x, max_x, min_y, max_y)
        objects.append(stick_mesh_pos)

    # Place bushes
    for _ in range(num_bushes):
        bush = create_bush(scale=bushes_scale)
        bush_mesh_pos = position_object_on_terrain(bush, terrain, min_x, max_x, min_y, max_y)
        objects.append(bush_mesh_pos)

    # Combine terrain and all objects into one mesh
    combined_mesh = trimesh.util.concatenate([terrain] + objects)
    return combined_mesh

def position_object_on_terrain(object_mesh, terrain, min_x, max_x, min_y, max_y, sink_depth=0.1):
    random_x = np.random.uniform(min_x, max_x)
    random_y = np.random.uniform(min_y, max_y)
    # Cast a ray downwards at (random_x, random_y) to find the correct z position
    ray_origins = np.array([[random_x, random_y, terrain.bounds[1][2] + 1000]])
    ray_directions = np.array([[0, 0, -1]])
    locations, index_ray, index_tri = terrain.ray.intersects_location(
        ray_origins=ray_origins,
        ray_directions=ray_directions
    )
    if locations.size > 0:
        correct_z = locations[0][2]
    else:
        correct_z = terrain.bounds[0][2]

    # Adjust Z position of the object to sink it slightly into the ground
    min_object_z = object_mesh.bounds[0][2]
    # Subtract sink_depth to embed the object into the ground
    translation = [random_x, random_y, correct_z - min_object_z - sink_depth]
    object_mesh.apply_translation(translation)
    return object_mesh

def save_combined_mesh(combined_mesh, file_name='combined_terrain_with_objects.stl'):
    # Save the combined mesh to a new STL file for preview
    combined_mesh.export(file_name)

    # Save the combined mesh in the location of user choice
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(defaultextension=".stl", filetypes=[("STL files", "*.stl")])
    if file_path:
        combined_mesh.export(file_path)

if __name__ == "__main__":
    num_rocks = 0
    points_per_rock = 1000
    rock_scale_min = 0.05
    rock_scale_max = 0.1
    
    num_trees = 0
    tree_scale = 0.1

    num_mushrooms = 0
    mushroom_scale = 0.2

    num_anthills = 0
    anthill_scale = 0.5

    num_sticks = 0
    stick_scale = 0.2

    num_bushes = 0
    bushes_scale = 1

    combined_mesh = place_objects_on_terrain('exported_mesh.stl', num_rocks, points_per_rock, rock_scale_min, rock_scale_max, num_trees, tree_scale, num_mushrooms, mushroom_scale, num_anthills, anthill_scale, num_sticks, stick_scale, num_bushes, bushes_scale)
    save_combined_mesh(combined_mesh)
