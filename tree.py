import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

def generate_random_tree():
    trunk_height = np.random.uniform(2, 5)
    trunk_radius = np.random.uniform(0.1, 0.3)
    
    # Ensure leaf dimensions are greater than trunk dimensions
    leaf_height = np.random.uniform(trunk_height + 1, trunk_height + 3)
    leaf_base_radius = np.random.uniform(trunk_radius + 0.2, trunk_radius + 0.5)
    
    trunk_resolution = 100
    trunk_z = np.linspace(0, trunk_height, 2)
    trunk_theta = np.linspace(0, 2*np.pi, trunk_resolution)
    trunk_theta, trunk_z = np.meshgrid(trunk_theta, trunk_z)
    trunk_x = trunk_radius * np.cos(trunk_theta)
    trunk_y = trunk_radius * np.sin(trunk_theta)
    
    leaf_resolution = 100
    leaf_z = np.linspace(trunk_height, trunk_height + leaf_height, 2)
    leaf_theta = np.linspace(0, 2*np.pi, leaf_resolution)
    leaf_theta, leaf_z = np.meshgrid(leaf_theta, leaf_z)
    leaf_radius = leaf_base_radius * (1 - leaf_z / (trunk_height + leaf_height))
    leaf_x = leaf_radius * np.cos(leaf_theta)
    leaf_y = leaf_radius * np.sin(leaf_theta)
    
    return trunk_x, trunk_y, trunk_z, leaf_x, leaf_y, leaf_z

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Generate and plot random trees
for _ in range(5):
    trunk_x, trunk_y, trunk_z, leaf_x, leaf_y, leaf_z = generate_random_tree()
    ax.plot_surface(trunk_x, trunk_y, trunk_z, color='brown')
    ax.plot_surface(leaf_x, leaf_y, leaf_z, color='green')

# Set plot limits and labels
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(0, 10)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Show the 3D trees
plt.show()
