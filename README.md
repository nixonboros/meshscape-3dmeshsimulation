# MeshScape: Advanced 3D Terrain Generation and Simulation

MeshScape is a sophisticated parametric 3D terrain generation tool designed for robotics simulation and 3D modeling applications. By combining procedural noise algorithms with dynamic object placement, it enables the creation of realistic and customizable 3D environments for simulation purposes. The tool features real-time visualization and configurable parameters, making it ideal for testing and validating robotic systems in various terrain conditions.

## Features

### Advanced Terrain Generation
- Multiple configurable noise algorithms (Perlin, Simplex, Value, Cellular)
- Parametric terrain customization:
  - Resolution control for simulation accuracy
  - Base elevation adjustment
  - Height range configuration
  - Noise scale and detail control
  - Octave-based detail layering
  - Persistence and lacunarity settings

### Dynamic Object Placement
- Procedural placement of environmental elements:
  - Trees with customizable density and scale
  - Rocks with variable size ranges and complexity
  - Sticks and natural debris
  - Bushes and vegetation
  - Anthills and terrain mounds
  - Small plants and ground cover

### Real-time Visualization
- Interactive 3D visualization using PyVista
- Dynamic parameter updates
- Real-time object count tracking
- Customizable view angles and perspectives
- Export capabilities for STL/3DS file formats

### User Interface
- Modern, responsive GUI built with CustomTkinter
- Intuitive parameter controls
- Comprehensive tooltips and help system
- Preset system for saving and loading configurations
- Real-time parameter feedback

### Technical Highlights
- Multi-threaded processing for smooth UI experience
- STL/3DS mesh generation and manipulation
- Real-time object count tracking
- Customizable mesh resolution
- Efficient memory management for large terrain generation
- Seamless integration with robotics simulation frameworks

## Technical Stack
- Python 3.x
- NumPy for numerical operations
- PyVista for 3D visualization
- SciPy for scientific computing
- CustomTkinter for modern UI
- Matplotlib for additional visualization
- PyQt5 for advanced UI components
- STL/3DS file processing libraries

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nixonboros/MeshScape-3D-Mesh-Simulation.git
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python meshgenGUI.py
```

## Usage

1. Configure terrain parameters in the "Noise" tab
2. Adjust terrain properties in the "Terrain" tab
3. Enable and configure objects in the "Objects" tab
4. Click "Generate Mesh" to create your terrain
5. Save and load configurations using the preset system
6. Export the generated terrain for use in robotics simulation
