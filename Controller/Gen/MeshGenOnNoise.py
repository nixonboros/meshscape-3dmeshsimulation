# Ensure the necessary packages are installed:
# pip install: numpy, Pillow pyvista, scipy, PyQt5, pyvistaqt

import sys
import numpy as np
import PIL.Image as Image
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
import pyvista as pv
from pyvistaqt import QtInteractor
from scipy.interpolate import griddata
import os
import aspose.threed as a3d

def load_image(image_path):
    with Image.open(image_path) as img:
        img = img.convert('L')  # Convert to grayscale
        heightmap = np.array(img)
    return heightmap

def create_mesh(heightmap, height_scale, height_offset, resolution_factor, base_elevation, min_height):
    y_orig, x_orig = np.indices(heightmap.shape)
    x = np.linspace(0, heightmap.shape[1] - 1, int(heightmap.shape[1] * resolution_factor))
    y = np.linspace(0, heightmap.shape[0] - 1, int(heightmap.shape[0] * resolution_factor))
    x_new, y_new = np.meshgrid(x, y)
    points = np.vstack((y_orig.ravel(), x_orig.ravel())).T
    values = heightmap.ravel()
    z = griddata(points, values, (y_new, x_new), method='cubic', fill_value=min_height)

    # Apply transformations
    z = z * height_scale + height_offset + base_elevation
    z = np.maximum(z, min_height)
    z = np.power(z, 1.2)

    # Create the terrain mesh
    grid = pv.StructuredGrid(x_new, y_new, z)
    terrain_mesh = grid.extract_surface()

    # Create a solid base layer
    base_layer = pv.Plane(center=(np.mean(x_new), np.mean(y_new), min_height),
                          i_size=x_new.ptp(), j_size=y_new.ptp(),
                          i_resolution=int(x_new.shape[1]), j_resolution=int(y_new.shape[0]))

    return terrain_mesh, base_layer

# class MainWindow(QMainWindow):
#     def __init__(self, terrain_mesh, base_layer):
#         super().__init__()
#         self.terrain_mesh = terrain_mesh
#         self.base_layer = base_layer
#         self.initUI()

#     def initUI(self):
#         self.setWindowTitle("Mesh Viewer and Exporter")
#         self.setGeometry(100, 100, 800, 600)
#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)
#         layout = QVBoxLayout(central_widget)
#         self.button = QPushButton('Export Mesh')
#         self.button.clicked.connect(self.export_mesh)
#         layout.addWidget(self.button)
#         self.frame = QtInteractor(central_widget)
#         layout.addWidget(self.frame)
#         self.frame.add_mesh(self.terrain_mesh, color='wheat')
#         self.frame.add_mesh(self.base_layer, color='blue')

#     def export_mesh(self):
#         filename = 'Temp/Exported_Mesh.stl'                       
#         self.terrain_mesh.save(filename)
#         print(f"Mesh exported successfully to {filename}")


def MeshGenOnNoise(resolution_factor, base_elevation, min_height, max_height):
    # resolution_factor = 1.5
    # base_elevation = 5
    # min_height = 0
    # max_height = 50

    script_dir = os.path.dirname(__file__)
    temp_dir = os.path.join(script_dir, 'Temp')

    # app = QApplication(sys.argv)
    image_path = os.path.join(temp_dir, 'Noise.png')     
    print("Exporting mesh...")
    # print("Mesh Parameter Values: " + resolution_factor  + " " + base_elevation + " " + min_height + " " + max_height)           
    heightmap = load_image(image_path)
    height_scale = max_height / heightmap.max()
    height_offset = -max_height / 2
    terrain_mesh, base_layer = create_mesh(heightmap, height_scale, height_offset, resolution_factor, base_elevation, min_height)
    # ex = MainWindow(terrain_mesh, base_layer)
    # ex.show()
    # sys.exit(app.exec_())

    # filename = 'Temp/Exported_Mesh.stl'                       
    terrain_mesh.save(os.path.join(temp_dir, "Exported_Mesh.stl"))
    print(f"Exported_Mesh.stl exported successfully to {temp_dir}")

    scene = a3d.Scene.from_file(os.path.join(temp_dir, "Exported_Mesh.stl"))
    scene.save(os.path.join(temp_dir, "Exported_Mesh.3ds"))
    print(f"Exported_Mesh.3ds exported successfully to {temp_dir}")

if __name__ == '__main__':
    MeshGenOnNoise()
