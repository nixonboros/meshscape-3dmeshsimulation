#pip install numpy and noise and matplotlib and pillow and scipy
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from noise import pnoise2, snoise2
from scipy.spatial import Voronoi, voronoi_plot_2d

def generate_noise_image(width, height, scale=100, octaves=6, persistence=0.5, lacunarity=2.0, seed=0, noise_type='perlin'):
    """
    Generate and save a 2D noise image with customizable variables.

    Parameters:
    - width, height: Dimensions of the generated image.
    - scale: Affects the "zoom" level of the noise.
    - octaves: Number of passes for generating noise, adds detail.
    - persistence, lacunarity: Affect the appearance of the noise.
    - seed: Seed for the noise generation.
    - noise_type: Type of the noise ('perlin', 'simplex', 'value', 'cellular').

    Returns:
    - A 2D numpy array of the generated noise.
    """
    noise_img = np.zeros((height, width))

    if noise_type in ['perlin', 'simplex']:
        for i in range(height):
            for j in range(width):
                x, y = i / scale, j / scale
                if noise_type == 'perlin':
                    noise_value = pnoise2(x, y, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=width, repeaty=height, base=seed)
                elif noise_type == 'simplex':
                    noise_value = snoise2(x, y, octaves=octaves, persistence=persistence, lacunarity=lacunarity, base=seed)
                noise_img[i][j] = noise_value
    elif noise_type == 'value':
        # Simple value noise implementation
        np.random.seed(seed)
        noise_img = np.random.rand(height, width)
    elif noise_type == 'cellular':
        # Generate points for Voronoi diagram
        points = np.random.rand(100, 2) * [width, height]  # Adjust number of points for different effects
        vor = Voronoi(points)
        for i, (x, y) in enumerate(points):
            noise_img[int(y)][int(x)] = 1  # Mark points
        # This is a very basic approximation and won't look exactly like cellular noise
        # Further processing is needed for a true cellular noise effect

    # Normalize to 0-255 and convert to uint8
    noise_img = np.interp(noise_img, (noise_img.min(), noise_img.max()), (0, 255)).astype(np.uint8)
    return noise_img

def save_image(image_array, file_name='noise_image.png'):
    """
    Save a 2D numpy array as an image.
    """
    img = Image.fromarray(image_array)
    img.save(file_name)

# Example usage
width, height = 600, 400
noise_type = 'simplex'  # Change to 'perlin', 'simplex', 'value', 'cellular'
noise_img = generate_noise_image(width, height, scale=50, octaves=6, persistence=0.5, lacunarity=2.0, seed=np.random.randint(0, 100), noise_type=noise_type)
save_image(noise_img, f'C:\\Users\\Ben\\Desktop\\{noise_type}_noise.png')
#^ may not work on non-macs, but need to specify file location here
#save_image(noise_img, f'{noise_type}_noise.png')

# Display the generated noise image
plt.figure(figsize=(10, 6))
plt.imshow(noise_img, cmap='gray')
plt.title(f"{noise_type.capitalize()} Noise")
plt.colorbar()
plt.show()