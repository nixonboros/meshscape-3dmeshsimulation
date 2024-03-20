import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

def generate_bush_points(center, min_radius, max_radius, num_points, length, density, lumpiness):
    # Generate spherical coordinates
    phi = np.random.uniform(0, 2 * np.pi, num_points)
    costheta = np.random.uniform(-1, 1, num_points)
    u = np.random.uniform(min_radius**3, max_radius**3, num_points)
    
    # Convert to cartesian coordinates
    theta = np.arccos(costheta)
    r = u**(1/3) * (1 + lumpiness * np.random.uniform(-0.5, 0.5, num_points)) 
    x = r * np.sin(theta) * np.cos(phi) + center[0]
    y = r * np.sin(theta) * np.sin(phi) + center[1] * length
    z = r * np.cos(theta) + center[2]

    # Density of the bush randomised through discarding points
    mask = np.random.uniform(0, 1, num_points) < density
    return x[mask], y[mask], z[mask]

def generate_sticks(center, num_sticks, stick_length, max_radius, stick_width):
    stick_points = []
    for _ in range(num_sticks):
        # Random position for each stick
        stick_center = np.array([
            np.random.uniform(center[0], max_radius / 2),
            np.random.uniform(center[1], max_radius / 2),
            np.random.uniform(center[2], max_radius / 2)
        ])

        # Random 3D orientation of sticks
        orientation = np.random.normal(0, np.pi, 3)
        for point in np.linspace(-stick_length / 2, stick_length / 2, int(stick_width)):
            dx = np.sin(orientation[0]) * np.cos(orientation[1]) * point
            dy = np.sin(orientation[0]) * np.sin(orientation[1]) * point
            dz = np.cos(orientation[0]) * point
            stick_points.append(stick_center + np.array([dx, dy, dz]))
    
    return np.array(stick_points).T


# Parameters for bush
center = [0, 0, 0]                               # Center of the bush
min_radius = random.uniform(0.5, 3)              # Minimum radius randomisation
max_radius = random.uniform(1.5, 3)              # Maximum radius randomisation
num_points = random.randint(1000, 3000)          # Total points to generate before sparsity is applied
length = random.uniform(0.5, 3.0)                # Elongates the bush in the Y direction
density = random.uniform(0.4, 1)                 # density randomiser
lumpiness = random.uniform(0.1, 0.5)             # Variation in radius to create lumps

# Parameters for stick
num_sticks = random.randint(5,10)
stick_length = random.uniform (0.5,1)
stick_width = random.randint(5, 20)

# Generate Bush
x, y, z = generate_bush_points(center, min_radius, max_radius, num_points, length, density, lumpiness)

#Generate Stick
sticks_x, sticks_y, sticks_z = generate_sticks(center, num_sticks, stick_length, stick_width, max_radius)

# Combine Bush and Stick
x = np.concatenate([x, sticks_x])
y = np.concatenate([y, sticks_y])
z = np.concatenate([z, sticks_z])

# Visualization
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, marker='o')
ax.set_xlabel('X Label')
ax.set_ylabel('Y Label')
ax.set_zlabel('Z Label')
plt.show()
