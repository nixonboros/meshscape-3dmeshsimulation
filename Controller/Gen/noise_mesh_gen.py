import sys
import numpy as np
import PIL.Image as Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyvista as pv
from pyvistaqt import QtInteractor
from scipy.interpolate import griddata
from stl import mesh
import os

# Get the application directory (works for both development and EXE)
if getattr(sys, 'frozen', False):
    # If running as EXE
    APP_DIR = os.path.dirname(sys.executable)
else:
    # If running in development
    APP_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Get the data directory path
DATA_DIR = os.path.join(APP_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

def load_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('L')  # Convert to grayscale
        heightmap = np.array(img)
    return heightmap

def create_mesh(heightmap, height_scale, height_offset, resolution_factor, base_elevation, floor_elevation, filename=None):
    if filename is None:
        filename = os.path.join(DATA_DIR, 'exported_mesh.stl')
    
    y_orig, x_orig = np.indices(heightmap.shape)
    x = np.linspace(0, heightmap.shape[1] - 1, int(heightmap.shape[1] * resolution_factor))
    y = np.linspace(0, heightmap.shape[0] - 1, int(heightmap.shape[0] * resolution_factor))
    x_new, y_new = np.meshgrid(x, y)
    points = np.vstack((y_orig.ravel(), x_orig.ravel())).T
    values = heightmap.ravel()
    z = griddata(points, values, (y_new, x_new), method='cubic', fill_value=floor_elevation)

    # Apply transformations
    z = z * height_scale + height_offset + base_elevation
    z = np.maximum(z, floor_elevation)
    z = np.power(z, 1.2)

    # Create the terrain mesh
    grid = pv.StructuredGrid(x_new, y_new, z)
    terrain_mesh = grid.extract_surface()
    terrain_mesh.save(filename)  # Save the mesh as an STL file automatically
    print(f"Mesh saved to {filename}")

    # Create a solid base layer
    base_layer = pv.Plane(center=(np.mean(x_new), np.mean(y_new), floor_elevation),
                          i_size=np.ptp(x_new), j_size=np.ptp(y_new),
                          i_resolution=int(x_new.shape[1]), j_resolution=int(y_new.shape[0]))

    return terrain_mesh, base_layer

class MainWindow(QMainWindow):
    def __init__(self, terrain_mesh, base_layer):
        super().__init__()
        self.terrain_mesh = terrain_mesh
        self.base_layer = base_layer
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mesh Viewer and Exporter")
        self.setGeometry(100, 100, 800, 600)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        self.button = QPushButton('Export Mesh')
        self.button.clicked.connect(self.export_mesh)
        layout.addWidget(self.button)
        self.frame = QtInteractor(central_widget)
        layout.addWidget(self.frame)
        self.frame.add_mesh(self.terrain_mesh, color='wheat')
        self.frame.add_mesh(self.base_layer, color='blue')

    def export_mesh(self):
        filename = 'another_exported_mesh.stl'  # Optionally allow re-export with a different name
        self.terrain_mesh.save(filename)
        #print(f"Mesh re-exported successfully to {filename}")

def generate_mesh_noise(resolution_factor, base_elevation, height_difference, floor_elevation, noise_image_location):

    #Default values
    #resolution_factor = 10
    #base_elevation = 0.5
    #height_difference = 1
    #floor_elevation = 0.5

    app = QApplication(sys.argv)
    image_path = noise_image_location
    heightmap = load_image(image_path)
    height_scale = height_difference / heightmap.max()
    height_offset = -height_difference / 2
    terrain_mesh, base_layer = create_mesh(heightmap, height_scale, height_offset, resolution_factor, base_elevation, floor_elevation)
    return

#if __name__ == '__main__':
#    main()
