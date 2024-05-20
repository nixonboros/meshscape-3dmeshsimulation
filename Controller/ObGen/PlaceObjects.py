import numpy as np
import trimesh

from .OakGen import mushroom_mesh
from .TreeGen import generate_tree, tree_to_trimesh
from .RockGen import rock_generator
from .AntHillGen import generate_anthill_mesh

def place_objects_on_terrain(terrain_path, num_rocks=5, points_per_rock=1000, rock_scale_min=0.05, rock_scale_max=0.1, num_trees=5, tree_scale=0.1, num_mushrooms=5, mushroom_scale=0.1, num_anthills=3, anthill_scale=1.0):
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
    # Save the combined mesh to a new STL file
    combined_mesh.export(file_name)

if __name__ == "__main__":
    num_rocks = 5
    points_per_rock = 1000
    rock_scale_min = 0.05
    rock_scale_max = 0.1
    
    num_trees = 50
    tree_scale = 0.1

    num_mushrooms = 5
    mushroom_scale = 0.2

    num_anthills = 3
    anthill_scale = 0.5
    
    combined_mesh = place_objects_on_terrain('exported_mesh.stl', num_rocks, points_per_rock, rock_scale_min, rock_scale_max, num_trees, tree_scale, num_mushrooms, mushroom_scale, num_anthills, anthill_scale)
    save_combined_mesh(combined_mesh)
