import sys
import os

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import customtkinter as ctk

import numpy as np
import threading
import time

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import art3d
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from stl import mesh
from functools import partial

from Controller.Gen.noisethingy import *
from Controller.Gen.noise_mesh_gen import *
from Controller.ObGen.PlaceObjects import *

matplotlib.use("TkAgg")

# Set the application icon
ICON_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "icon.ico")

def center_window(window, width=None, height=None):
    # Force window to update its geometry
    window.update_idletasks()
    
    # Get the window's current size if not specified
    if width is None:
        width = window.winfo_width()
    if height is None:
        height = window.winfo_height()
    
    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    # Calculate position for center of screen
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    # Set the window position
    window.geometry(f'+{x}+{y}')

# SPLASH SCREEN
splash_root = ctk.CTk()
splash_root.geometry("320x160")
splash_root.overrideredirect(True)
# Use a unique color for transparency
transparent_color = "#e9ecef"
splash_root.configure(bg=transparent_color)
splash_root.wm_attributes("-transparentcolor", transparent_color)

# Set icon for splash screen if it exists
if os.path.exists(ICON_PATH):
    splash_root.iconbitmap(ICON_PATH)

# Center the splash window with explicit size
center_window(splash_root, 320, 160)

# Centering helper frame
center_frame = ctk.CTkFrame(splash_root, fg_color=transparent_color, corner_radius=0)
center_frame.pack(expand=True, fill="both")

# Card-style splash frame (smaller)
frame_splash = ctk.CTkFrame(center_frame, fg_color="white", corner_radius=14, border_width=2, border_color="#4e84ae")
frame_splash.pack(expand=True, padx=10, pady=10)

# TITLE LABEL (less padding)
splash_label = ctk.CTkLabel(
    frame_splash,
    text="Loading...",
    font=ctk.CTkFont(size=18, weight="bold"),
    text_color="#4e84ae",
    width=200,
    height=50
)
splash_label.pack(padx=10, pady=(16, 6))

# Splash Loading Bar
splash_bar = ctk.CTkProgressBar(frame_splash, width=110, height=10)
splash_bar.pack(pady=(0, 12))
splash_bar.set(0)

def animate_splash_bar(progress=0):
    if progress < 1.0:
        splash_bar.set(progress)
        splash_root.after(20, animate_splash_bar, progress + 0.02)
    else:
        splash_bar.set(1.0)
        splash_root.after(200, main_window)

# Start the animation
animate_splash_bar()

# --- Make splash window draggable ---
_drag_data = {'x': 0, 'y': 0}

def start_move(event):
    _drag_data['x'] = event.x
    _drag_data['y'] = event.y

def do_move(event):
    x = splash_root.winfo_x() + event.x - _drag_data['x']
    y = splash_root.winfo_y() + event.y - _drag_data['y']
    splash_root.geometry(f'+{x}+{y}')

frame_splash.bind('<Button-1>', start_move)
frame_splash.bind('<B1-Motion>', do_move)

# MAIN WINDOW
root = ctk.CTk()
root.title("MeshScape")
root.geometry("1366x768")
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")  
root.configure(fg_color="#f7f9fb")   
root.columnconfigure(0, weight=1)

# Set icon for main window if it exists
if os.path.exists(ICON_PATH):
    root.iconbitmap(ICON_PATH)
    # Set taskbar icon
    root.wm_iconbitmap(ICON_PATH)
    # Ensure the icon is visible in the taskbar
    root.wm_attributes('-toolwindow', False)

# Center the main window with explicit size
center_window(root, 1366, 768)

def main_window():
#to connect to sliders
    root.withdraw()
    splash_root.after(4000, splash_root.destroy)
    root.after(4500, root.deiconify)
    def add_objects_to_mesh(): 
        progress_bar.set(0.0)

        num_rocks = int(rocks_slider.get())
        points_per_rock = int(rocks_point_slider.get())
        rock_scale_min = float(rocks_min_slider.get() / 100)
        rock_scale_max = float(rocks_max_slider.get() / 100)
        
        num_trees = int(trees_slider.get())
        tree_scale = float(trees_scale_slider.get() / 100)

        num_mushrooms = int(mushroom_slider.get())
        mushroom_scale = float(mushroom_scale_slider.get() / 100)

        num_anthills = int(volcano_slider.get())
        anthill_scale = float(volcano_scale_slider.get() / 100)

        num_sticks = int(sticks_slider.get())
        stick_scale = float(sticks_scale_slider.get() / 100)
        
        num_bushes = int(bushes_slider.get())
        bushes_scale = float(bushes_scale_slider.get() / 50)

        if (add_trees_switch.get() == "off"):
            num_trees = 0
        if (add_rocks_switch.get() == "off"):
            num_rocks = 0
        if (add_sticks_switch.get() == "off"):
            num_sticks = 0
        if (add_bushes_switch.get() == "off"):
            num_bushes = 0
        if (add_volcano_switch.get() == "off"):
            num_anthills = 0
        if (add_mushroom_switch.get() == "off"):
            num_mushrooms = 0

        progress_bar.set(0.6)
        combined_mesh = place_objects_on_terrain('exported_mesh.stl', num_rocks, points_per_rock, 
                                                rock_scale_min, rock_scale_max, num_trees, 
                                                tree_scale, num_mushrooms, mushroom_scale, 
                                                num_anthills, anthill_scale, num_sticks, 
                                                stick_scale, num_bushes, bushes_scale)
        
        root.after(0, save_combined_mesh, combined_mesh)

    def generate_noise():
        def run_long_task():
            try:
                progress_bar.set(0.0)

                noise_image_location = export_image(
                    int(width_slider.get()),
                    int(height_slider.get()),
                    int(scale_slider.get()),
                    int(octaves_slider.get()),
                    int(persistence_slider.get()),
                    int(lacunarity_slider.get()),
                    np.random.randint(0, 100),
                    noise_type_dropdown.get(),
                )
                
                progress_bar.set(0.3)
                generate_mesh_noise(
                    int(resolution_factor_slider.get()),
                    float(base_elevation_slider.get()/200),
                    float((max_height_slider.get()-min_height_slider.get())/200),
                    float(min_height_slider.get()/200),
                    noise_image_location
                )
                progress_bar.set(0.6)
                
                root.after(50, add_objects_to_mesh)
                root.after(50, partial(messagebox.showinfo, "Success", "Mesh creation is complete!"))

                progress_bar.set(0.8)

                root.after(50, run_visualization)

                progress_bar.set(1.0)

            except Exception as e:
                root.after(0, messagebox.showerror, "Error", f"An error occurred: {str(e)}")
            finally:
                progress_bar.set(0)

        threading.Thread(target=run_long_task).start()

    def update_slider_label(label, text, value):
        label.configure(text=f"{text}: {int(value)}")
        update_object_count()


    def toggle_visibility(
        switch_variable, *slider_and_labels, frame
    ):
        if switch_variable.get() == "on":
            for i in range(0, len(slider_and_labels), 2):
                slider_label, slider = slider_and_labels[i], slider_and_labels[i+1]
                slider_label.grid(row=1 + i, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
                slider.grid(row=1 + i, column=1, padx=10, pady=(0, 10), sticky="ew")
            frame.configure(fg_color="#d1d1d1")
        else:
            for i in range(0, len(slider_and_labels), 2):
                slider_label, slider = slider_and_labels[i], slider_and_labels[i+1]
                slider_label.grid_forget()
                slider.grid_forget()
            frame.configure(fg_color="#dfe1e1")


    # Save preset function
    def save_preset():
        # Get all parameter values
        preset_data = {
            "noise_type": noise_type_dropdown.get(),
            "width": width_slider.get(),
            "height": height_slider.get(),
            "scale": scale_slider.get(),
            "octaves": octaves_slider.get(),
            "persistence": persistence_slider.get(),
            "lacunarity": lacunarity_slider.get(),
            "resolution_factor": resolution_factor_slider.get(),
            "base_elevation": base_elevation_slider.get(),
            "min_height": min_height_slider.get(),
            "max_height": max_height_slider.get(),
            "add_trees": add_trees_switch.get(),
            "trees_density": trees_slider.get(),
            "trees_scale": trees_scale_slider.get(),
            "add_rocks": add_rocks_switch.get(),
            "rocks_min": rocks_min_slider.get(),
            "rocks_max": rocks_max_slider.get(),
            "rocks_point": rocks_point_slider.get(),
            "rocks_density": rocks_slider.get(),
            "add_sticks": add_sticks_switch.get(),
            "sticks_density": sticks_slider.get(),
            "sticks_scale": sticks_scale_slider.get(),
            "add_bushes": add_bushes_switch.get(),
            "bushes_scale": bushes_scale_slider.get(),
            "bushes_density": bushes_slider.get(),
            "add_volcano": add_volcano_switch.get(),
            "volcano_scale": volcano_scale_slider.get(),
            "volcano_density": volcano_slider.get(),
            "add_mushroom": add_mushroom_switch.get(),
            "mushroom_scale": mushroom_scale_slider.get(),
            "mushroom_density": mushroom_slider.get(),
        }
        # Open a file dialog for saving
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json", filetypes=[("JSON files", "*.json")]
        )
        if file_path:
            with open(file_path, "w") as f:
                json.dump(preset_data, f)
            # Update the option menu
            preset_name = os.path.basename(file_path)[:-5]
            presets_optionmenu.configure(
                values=presets_optionmenu.cget("values") + [preset_name]
            )
            presets_optionmenu.set(preset_name)

    # Load preset function
    def load_preset():
        # Open a file dialog for loading
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                preset_data = json.load(f)
            # Update all parameter values
            noise_type_dropdown.set(preset_data["noise_type"])
            width_slider.set(preset_data["width"])
            height_slider.set(preset_data["height"])
            scale_slider.set(preset_data["scale"])
            octaves_slider.set(preset_data["octaves"])
            persistence_slider.set(preset_data["persistence"])
            lacunarity_slider.set(preset_data["lacunarity"])
            resolution_factor_slider.set(preset_data["resolution_factor"])
            base_elevation_slider.set(preset_data["base_elevation"])
            min_height_slider.set(preset_data["min_height"])
            max_height_slider.set(preset_data["max_height"])
            
            # Update the labels
            update_slider_label(width_label, "Mesh Width", preset_data["width"])
            update_slider_label(height_label, "Mesh Height", preset_data["height"])
            update_slider_label(scale_label, "Zoom Scale", preset_data["scale"])
            update_slider_label(octaves_label, "Octaves", preset_data["octaves"])
            update_slider_label(persistence_label, "Persistence", preset_data["persistence"])
            update_slider_label(lacunarity_label, "Lacunarity", preset_data["lacunarity"])
            update_slider_label(resolution_factor_label, "Resolution Factor", preset_data["resolution_factor"])
            update_slider_label(base_elevation_label, "Base Elevation", preset_data["base_elevation"])
            update_slider_label(min_height_label, "Min Height", preset_data["min_height"])
            update_slider_label(max_height_label, "Max Height", preset_data["max_height"])
            
            # Update the option menu
            preset_name = os.path.basename(file_path)[:-5]
            presets_optionmenu.configure(
                values=presets_optionmenu.cget("values") + [preset_name]
            )
            presets_optionmenu.set(preset_name)


    def toggle_trees_visibility(*args):
        toggle_visibility(
            add_trees_switch,
            trees_slider,trees_slider_label,
            trees_scale_slider,trees_scale_slider_label,
            frame = frame_trees,
        )
        update_object_count()

    def toggle_rocks_visibility(*args):
        toggle_visibility(
            add_rocks_switch,
            rocks_slider,rocks_slider_label,
            rocks_point_slider, rocks_point_slider_label,
            rocks_min_slider, rocks_min_slider_label,
            rocks_max_slider, rocks_max_slider_label,
            frame = frame_rocks,
        )
        update_object_count()       

    def toggle_sticks_visibility(*args):
        toggle_visibility(
            add_sticks_switch,
            sticks_slider, sticks_slider_label,
            sticks_scale_slider, sticks_scale_slider_label,
            frame = frame_sticks,
        )
        update_object_count()

    def toggle_bushes_visibility(*args):
        toggle_visibility(
            add_bushes_switch,
            bushes_slider, bushes_slider_label,
            bushes_scale_slider, bushes_scale_slider_label,
            frame = frame_bushes,
        )
        update_object_count()

    def toggle_volcanos_visibility(*args):
        toggle_visibility(
            add_volcano_switch,
            volcano_slider, volcano_slider_label,
            volcano_scale_slider, volcano_scale_slider_label,
            frame = frame_volcanos,
        )
        update_object_count()

    def toggle_mushrooms_visibility(*args):
        toggle_visibility(
            add_mushroom_switch,
            mushroom_slider, mushroom_slider_label,
            mushroom_scale_slider, mushroom_scale_slider_label,
            frame = frame_mushrooms,
        )
        update_object_count()
        
    # Left Section
    left_section = ctk.CTkFrame(root, corner_radius=16, border_width=1, border_color="#e0e6ed", fg_color="#ffffff")
    left_section.grid(row=0, column=0, padx=(16, 16), pady=12, sticky="nsew")
    root.rowconfigure(0, weight=1)

    # Set the minimum width for the left section
    left_section.grid_columnconfigure(0, weight=1)

    #PROGRESS BAR
    progress_bar = ctk.CTkProgressBar(left_section, width=300)
    progress_bar.grid(row=4, column=0, columnspan=2, pady=(15, 15))
    progress_bar.set(0)

    # FRAME FOR TITLE LABEL
    frame_title = ctk.CTkFrame(
        left_section,
        fg_color="white",
        corner_radius=16,
        border_width=2,
        border_color="#e0e6ed"
    )
    frame_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 8), sticky="ew")
    frame_title.columnconfigure(0, weight=1)

    # TITLE LABEL
    title_label = ctk.CTkLabel(
        frame_title,
        text="MeshScape",
        font=ctk.CTkFont(size=28, weight="bold"),
        text_color="#4e84ae",
    )
    title_label.grid(row=0, column=0, pady=(18, 12))

    # PRESETS DROPDOWN MENU
    presets_label = ctk.CTkLabel(left_section, text="Preset:", font=ctk.CTkFont(size=15, weight="bold"), text_color="#4e84ae")
    presets_label.grid(row=1, column=0, padx=20, pady=(0, 0), sticky="w")

    presets_optionmenu = ctk.CTkOptionMenu(
        left_section,
        values=["Default"],
        width=180,
        fg_color="#e0e6ed",
        button_color="#4e84ae",
        button_hover_color="#62a5d9",
        font=ctk.CTkFont(size=14),
        dropdown_font=ctk.CTkFont(size=13),
        text_color="#222"
    )
    presets_optionmenu.grid(row=1, column=0, padx=(90, 0), pady=(0, 0), sticky="w")

    # SAVE PRESET BUTTON
    create_preset_button = ctk.CTkButton(
        left_section,
        text="Save",
        command=save_preset,
        width=60,
        height=28,
        corner_radius=8,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="#4e84ae",
        hover_color="#62a5d9",
        text_color="white"
    )
    create_preset_button.grid(row=1, column=0, padx=(285, 0), pady=(0, 0), sticky="w")

    # LOAD PRESET BUTTON
    load_preset_button = ctk.CTkButton(
        left_section,
        text="Load",
        command=load_preset,
        width=60,
        height=28,
        corner_radius=8,
        font=ctk.CTkFont(size=13, weight="bold"),
        fg_color="#4e84ae",
        hover_color="#62a5d9",
        text_color="white"
    )
    load_preset_button.grid(row=1, column=0, padx=(355, 0), pady=(0, 0), sticky="w")

    # Section divider for visual separation
    divider = ctk.CTkFrame(left_section, height=2, fg_color="#e0e6ed", corner_radius=1)
    divider.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=(4, 4))

    ############################################################################################################

    # TABVIEW
    tabview = ctk.CTkTabview(
        left_section,
        fg_color="#f7f9fb",
        segmented_button_fg_color="#e0e6ed",
        segmented_button_selected_color="#4e84ae",
        segmented_button_selected_hover_color="#62a5d9",
        segmented_button_unselected_color="#c5c9d1",
        segmented_button_unselected_hover_color="#aab0bb",
        corner_radius=12,
        border_width=1,
        border_color="#e0e6ed"
    )
    tabview.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(0, 0))

    tabview.add("Noise")
    tabview.add("Terrain")
    tabview.add("Objects")

    tabview.set("Noise")

    tabview.tab("Noise").columnconfigure(0, weight=1)
    tabview.tab("Terrain").columnconfigure(0, weight=1)
    tabview.tab("Objects").columnconfigure(0, weight=1)

    # Add section headers to each tab for clarity
    ctk.CTkLabel(tabview.tab("Noise"), text="Noise Settings", font=ctk.CTkFont(size=16, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, sticky="w", pady=(0, 8))
    ctk.CTkLabel(tabview.tab("Terrain"), text="Terrain Settings", font=ctk.CTkFont(size=16, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, sticky="w", pady=(0, 8))
    ctk.CTkLabel(tabview.tab("Objects"), text="Object Placement", font=ctk.CTkFont(size=16, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, sticky="w", pady=(0, 8))

    ############################################################################################################

    # Visualization function
    plt.switch_backend('agg')

    def visualize_stl():
        try:
            # Load the mesh
            your_mesh = mesh.Mesh.from_file('combined_terrain_with_objects.stl')

            # Simplify the mesh by taking every nth face (adjust the value of n for more/less simplification)
            n = 2
            simplified_vectors = your_mesh.vectors[::n]

            # Create the plot
            fig = plt.Figure(figsize=(5, 5))
            ax = fig.add_subplot(111, projection='3d')
            
            # Plot the simplified mesh
            poly3d = art3d.Poly3DCollection(simplified_vectors, alpha=0.5, edgecolor='k', linewidth=0.1)
            ax.add_collection3d(poly3d)
            
            # Auto scale to the mesh size
            scale = np.concatenate([your_mesh.min_, your_mesh.max_])
            ax.auto_scale_xyz(scale, scale, scale)

            # Set the view angle
            ax.view_init(elev=30, azim=45)
            
            # Hide axes for better visualization
            ax.set_axis_off()

            # Clear existing canvas if it exists
            for widget in frame_visualisation.winfo_children():
                widget.destroy()

            # Create a new canvas
            canvas = FigureCanvasTkAgg(fig, master=frame_visualisation)
            canvas.draw()
            widget = canvas.get_tk_widget()
            widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

            # Ensure right section maintains its width
            right_section.configure(width=500)
            right_section.grid_propagate(False)

        except Exception as e:
            print(e)

        # Function to run the visualization in the main thread
    def run_visualization():
        root.after(100, visualize_stl)

    # Setup right section and frame visualization
    right_section = ctk.CTkFrame(root, fg_color="#ffffff", corner_radius=16, border_width=1, border_color="#e0e6ed", width=500)
    right_section.grid(row=0, column=1, padx=(16, 16), pady=10, sticky="nsew")
    right_section.grid_propagate(False)  # Prevent the frame from shrinking
    right_section.columnconfigure(0, weight=1)

    frame_visualisation = ctk.CTkFrame(right_section, width=190, height=560, fg_color="white")
    frame_visualisation.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
    frame_visualisation.columnconfigure(0, weight=1)

    root.after(100, run_visualization)

    ############################################################################################################

    # FRAME_BASE_OBJECTS
    frame_objects_card = ctk.CTkScrollableFrame(
        tabview.tab("Objects"),
        fg_color="#ffffff",
        corner_radius=14,
        border_width=1,
        border_color="#e0e6ed",
        height=400
    )
    frame_objects_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
    frame_objects_card.columnconfigure(0, weight=1)

    # FRAME_TREES
    frame_trees = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_trees.grid(row=0, column=0, sticky="ew", padx=(0, 8), pady=(8))

    # FRAME_ROCKS
    frame_rocks = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_rocks.grid(row=1, column=0, padx=(0, 8), pady=(8), sticky="ew")

    # FRAME_STICKS
    frame_sticks = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_sticks.grid(row=2, column=0, padx=(0, 8), pady=(8), sticky="ew")

    # FRAME_BUSHES
    frame_bushes = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_bushes.grid(row=3, column=0, padx=(0, 8), pady=(8), sticky="ew")

    # FRAME_VOLCANOES
    frame_volcanos = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_volcanos.grid(row=4, column=0, padx=(0, 8), pady=(8), sticky="ew")

    # FRAME_MUSHROOMS
    frame_mushrooms = ctk.CTkFrame(
        frame_objects_card, border_width=0, fg_color="#dfe1e1", corner_radius=20
    )
    frame_mushrooms.grid(row=5, column=0, padx=(0, 8), pady=(8), sticky="ew")

    ############################################################################################################

    # ENABLE/DISABLE TREES SWITCH
    add_trees_switch = ctk.StringVar(value="off")
    add_trees_switch.trace_add(
        "write", toggle_trees_visibility
    )  # bind toggle_slider_visibility function to switch variable
    trees_switch = ctk.CTkSwitch(
        frame_trees,
        text="Trees",
        command=toggle_trees_visibility,
        variable=add_trees_switch,
        onvalue="on",
        offvalue="off",
    )
    trees_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # TREE SLIDERS
    trees_slider_label = ctk.CTkLabel(
        frame_trees, text="Density: 30", width=125, anchor="w"
    )
    trees_slider = ctk.CTkSlider(
        frame_trees,
        from_=0,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(trees_slider_label, "Density", value),
    )
    trees_slider.set(30)

    # TREE SCALE SLIDERS
    trees_scale_slider_label = ctk.CTkLabel(
        frame_trees, text="Scale: 10", width=125, anchor="w"
    )
    trees_scale_slider = ctk.CTkSlider(
        frame_trees,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(trees_scale_slider_label, "Scale", value),
    )
    trees_scale_slider.set(10)

    ############################################################################################################

    # ENABLE/DISABLE ADD ROCKS BUTTON
    add_rocks_switch = ctk.StringVar(value="off")
    add_rocks_switch.trace_add(
        "write", toggle_rocks_visibility
    )  # bind toggle_slider_visibility function to switch variable
    rocks_switch = ctk.CTkSwitch(
        frame_rocks,
        text="Rocks",
        command=toggle_rocks_visibility,
        variable=add_rocks_switch,
        onvalue="on",
        offvalue="off",
    )
    rocks_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # ROCKS SLIDERS
    rocks_slider_label = ctk.CTkLabel(
        frame_rocks, text="Density: 15", width=125, anchor="w"
    )
    rocks_slider = ctk.CTkSlider(
        frame_rocks,
        from_=0,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(rocks_slider_label, "Density", value),
    )
    rocks_slider.set(15)

    # ROCKS MIN SLIDERS
    rocks_min_slider_label = ctk.CTkLabel(
        frame_rocks, text="Min Size: 10", width=125, anchor="w"
    )
    rocks_min_slider = ctk.CTkSlider(
        frame_rocks,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(rocks_min_slider_label, "Min", value),
    )
    rocks_min_slider.set(10)

    # ROCKS MAX SLIDERS
    rocks_max_slider_label = ctk.CTkLabel(
        frame_rocks, text="Max Size: 15", width=125, anchor="w"
    )
    rocks_max_slider = ctk.CTkSlider(
        frame_rocks,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(rocks_max_slider_label, "Max", value),
    )
    rocks_max_slider.set(15)

    # ROCKS POINT SLIDERS
    rocks_point_slider_label = ctk.CTkLabel(
        frame_rocks, text="Points: 1000", width=125, anchor="w"
    )
    rocks_point_slider = ctk.CTkSlider(
        frame_rocks,
        from_=10,
        to=10000,
        width=330,  # make scalable to window
        number_of_steps=9990,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(rocks_point_slider_label, "Points", value),
    )
    rocks_point_slider.set(1000)

    ############################################################################################################

    # ENABLE/DISABLE ADD STICKS BUTTON
    add_sticks_switch = ctk.StringVar(value="off")
    add_sticks_switch.trace_add(
        "write", toggle_sticks_visibility
    )  # bind toggle_slider_visibility function to switch variable
    sticks_switch = ctk.CTkSwitch(
        frame_sticks,
        text="Sticks",
        command=toggle_sticks_visibility,
        variable=add_sticks_switch,
        onvalue="on",
        offvalue="off",
    )
    sticks_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # STICKS SLIDERS
    sticks_slider_label = ctk.CTkLabel(
        frame_sticks, text="Density: 50", width=125, anchor="w"
    )
    sticks_slider = ctk.CTkSlider(
        frame_sticks,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(sticks_slider_label, "Density", value),
    )
    sticks_slider.set(50)

    # STICK SCALE SLIDERS
    sticks_scale_slider_label = ctk.CTkLabel(
        frame_sticks, text="Scale: 10", width=125, anchor="w"
    )
    sticks_scale_slider = ctk.CTkSlider(
        frame_sticks,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(sticks_scale_slider_label, "Scale", value),
    )
    sticks_scale_slider.set(10)

    ############################################################################################################

    # ENABLE/DISABLE ADD BUSHES BUTTON
    add_bushes_switch = ctk.StringVar(value="off")
    add_bushes_switch.trace_add(
        "write", toggle_bushes_visibility
    )  # bind toggle_slider_visibility function to switch variable
    bushes_switch = ctk.CTkSwitch(
        frame_bushes,
        text="Bushes",
        command=toggle_bushes_visibility,
        variable=add_bushes_switch,
        onvalue="on",
        offvalue="off",
    )
    bushes_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # BUSHES SLIDERS
    bushes_slider_label = ctk.CTkLabel(
        frame_bushes, text="Density: 50", width=125, anchor="w"
    )
    bushes_slider = ctk.CTkSlider(
        frame_bushes,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(bushes_slider_label, "Density", value),
    )
    bushes_slider.set(50)

    # STICK SCALE SLIDERS
    bushes_scale_slider_label = ctk.CTkLabel(
        frame_bushes, text="Scale: 50", width=125, anchor="w"
    )
    bushes_scale_slider = ctk.CTkSlider(
        frame_bushes,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(bushes_scale_slider_label, "Scale", value),
    )
    bushes_scale_slider.set(50)

    ############################################################################################################

    # ENABLE/DISABLE ADD VOLCANO SWITCH
    add_volcano_switch = ctk.StringVar(value="off")
    add_volcano_switch.trace_add(
        "write", toggle_volcanos_visibility
    )  # bind toggle_slider_visibility function to switch variable
    volcano_switch = ctk.CTkSwitch(
        frame_volcanos,
        text="Anthills",
        command=toggle_volcanos_visibility,
        variable=add_volcano_switch,
        onvalue="on",
        offvalue="off",
    )
    volcano_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # VOLCANO SLIDERS
    volcano_slider_label = ctk.CTkLabel(
        frame_volcanos, text="Density: 10", width=125, anchor="w"
    )
    volcano_slider = ctk.CTkSlider(
        frame_volcanos,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(volcano_slider_label, "Density", value),
    )
    volcano_slider.set(10)

    # VOLCANO SCALE SLIDERS
    volcano_scale_slider_label = ctk.CTkLabel(
        frame_volcanos, text="Scale: 60", width=125, anchor="w"
    )
    volcano_scale_slider = ctk.CTkSlider(
        frame_volcanos,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(volcano_scale_slider_label, "Scale", value),
    )
    volcano_scale_slider.set(60)

    ############################################################################################################

    # ENABLE/DISABLE ADD MUSHROOM SWITCH
    add_mushroom_switch = ctk.StringVar(value="off")
    add_mushroom_switch.trace_add(
        "write", toggle_mushrooms_visibility
    )  # bind toggle_slider_visibility function to switch variable
    mushroom_switch = ctk.CTkSwitch(
        frame_mushrooms,
        text="Small Plants",
        command=toggle_mushrooms_visibility,
        variable=add_mushroom_switch,
        onvalue="on",
        offvalue="off",
    )
    mushroom_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    # MUSHROOM SLIDERS
    mushroom_slider_label = ctk.CTkLabel(
        frame_mushrooms, text="Density: 15", width=125, anchor="w"
    )
    mushroom_slider = ctk.CTkSlider(
        frame_mushrooms,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(mushroom_slider_label, "Density", value),
    )
    mushroom_slider.set(15)

    # MUSHROOM SCALE SLIDERS
    mushroom_scale_slider_label = ctk.CTkLabel(
        frame_mushrooms, text="Scale: 10", width=125, anchor="w"
    )
    mushroom_scale_slider = ctk.CTkSlider(
        frame_mushrooms,
        from_=1,
        to=100,
        width=330,  # make scalable to window
        number_of_steps=99,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(mushroom_scale_slider_label, "Scale", value),
    )
    mushroom_scale_slider.set(10)

    ############################################################################################################

    #OBJECT COUNTER

    def update_object_count():
        num_rocks = int(rocks_slider.get())
        num_trees = int(trees_slider.get())
        num_mushrooms = int(mushroom_slider.get())
        num_anthills = int(volcano_slider.get())
        num_sticks = int(sticks_slider.get())
        num_bushes = int(bushes_slider.get())

        if (add_trees_switch.get() == "off"):
            num_trees = 0
        if (add_rocks_switch.get() == "off"):
            num_rocks = 0
        if (add_sticks_switch.get() == "off"):
            num_sticks = 0
        if (add_bushes_switch.get() == "off"):
            num_bushes = 0
        if (add_volcano_switch.get() == "off"):
            num_anthills = 0
        if (add_mushroom_switch.get() == "off"):
            num_mushrooms = 0
        
        total_objects = num_rocks + num_trees + num_mushrooms + num_anthills + num_sticks + num_bushes
        object_count_label.configure(text=f"Total Objects: {total_objects}")

    object_count_label = ctk.CTkLabel(right_section, text="Total Objects: 0", font=ctk.CTkFont(size=14, weight="bold"))
    object_count_label.grid(row=1, column=0, pady=(10, 10), padx=10, sticky="s")

    update_object_count()

    ############################################################################################################

    # Noise Card
    frame_noise_card = ctk.CTkFrame(
        tabview.tab("Noise"),
        fg_color="#ffffff",
        corner_radius=14,
        border_width=1,
        border_color="#e0e6ed"
    )
    frame_noise_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
    tabview.tab("Noise").grid_columnconfigure(0, weight=1)
    frame_noise_card.grid_columnconfigure(0, weight=1)
    frame_noise_card.grid_columnconfigure(1, weight=1)
    frame_noise_card.grid_columnconfigure(2, weight=0)

    # 1. Noise Type Group (left-aligned like other groups)
    noise_type_group = ctk.CTkFrame(frame_noise_card, fg_color="transparent", corner_radius=10)
    noise_type_group.grid(row=0, column=0, columnspan=3, sticky="ew", padx=8, pady=(16, 0))
    noise_type_group.grid_columnconfigure(0, weight=0)
    noise_type_group.grid_columnconfigure(1, weight=0)
    noise_type_label = ctk.CTkLabel(
        noise_type_group, text="Noise Type", font=ctk.CTkFont(size=13), anchor="e"
    )
    noise_type_label.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=8)
    noise_type_dropdown = ctk.CTkOptionMenu(
        noise_type_group,
        values=['Perlin', 'Simplex', 'Value', 'Cellular'],
        width=120,
        fg_color="#e0e6ed",
        button_color="#4e84ae",
        button_hover_color="#62a5d9",
        font=ctk.CTkFont(size=13),
        dropdown_font=ctk.CTkFont(size=12),
        text_color="#222"
    )
    noise_type_dropdown.grid(row=0, column=1, sticky="w", padx=0, pady=8)
    noise_type_dropdown.set("Perlin")

    # 2. Mesh Size Group
    mesh_size_group = ctk.CTkFrame(frame_noise_card, fg_color="transparent", corner_radius=10)
    mesh_size_group.grid(row=1, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 0))
    mesh_size_group.grid_columnconfigure(0, weight=0)
    mesh_size_group.grid_columnconfigure(1, weight=1)
    mesh_size_group.grid_columnconfigure(2, weight=0)
    ctk.CTkLabel(mesh_size_group, text="Mesh Size", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(8, 4))
    # Mesh Width
    width_label = ctk.CTkLabel(mesh_size_group, text="Mesh Width", font=ctk.CTkFont(size=13), anchor="e")
    width_label.grid(row=1, column=0, sticky="e", padx=(16, 8), pady=4)
    width_value = ctk.CTkLabel(mesh_size_group, text="15", font=ctk.CTkFont(size=13), width=32, anchor="w")
    width_value.grid(row=1, column=2, sticky="w", padx=(8, 16), pady=4)
    def update_width(val):
        width_value.configure(text=f"{int(val)}")
        update_object_count()
    width_slider = ctk.CTkSlider(
        mesh_size_group,
        from_=10,
        to=50,
        width=220,
        number_of_steps=50,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_width,
    )
    width_slider.grid(row=1, column=1, sticky="ew", padx=0, pady=4)
    width_slider.set(15)
    # Mesh Height
    height_label = ctk.CTkLabel(mesh_size_group, text="Mesh Height", font=ctk.CTkFont(size=13), anchor="e")
    height_label.grid(row=2, column=0, sticky="e", padx=(16, 8), pady=(4, 8))
    height_value = ctk.CTkLabel(mesh_size_group, text="15", font=ctk.CTkFont(size=13), width=32, anchor="w")
    height_value.grid(row=2, column=2, sticky="w", padx=(8, 16), pady=(4, 8))
    def update_height(val):
        height_value.configure(text=f"{int(val)}")
        update_object_count()
    height_slider = ctk.CTkSlider(
        mesh_size_group,
        from_=10,
        to=50,
        width=220,
        number_of_steps=50,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_height,
    )
    height_slider.grid(row=2, column=1, sticky="ew", padx=0, pady=(4, 8))
    height_slider.set(15)

    # 3. Scale Group
    scale_group = ctk.CTkFrame(frame_noise_card, fg_color="transparent", corner_radius=10)
    scale_group.grid(row=2, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 0))
    scale_group.grid_columnconfigure(0, weight=0)
    scale_group.grid_columnconfigure(1, weight=1)
    scale_group.grid_columnconfigure(2, weight=0)
    ctk.CTkLabel(scale_group, text="Scale", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(8, 4))
    # Zoom Scale
    scale_label = ctk.CTkLabel(scale_group, text="Zoom Scale", font=ctk.CTkFont(size=13), anchor="e")
    scale_label.grid(row=1, column=0, sticky="e", padx=(16, 8), pady=(4, 8))
    scale_value = ctk.CTkLabel(scale_group, text="100", font=ctk.CTkFont(size=13), width=32, anchor="w")
    scale_value.grid(row=1, column=2, sticky="w", padx=(8, 16), pady=(4, 8))
    def update_scale(val):
        scale_value.configure(text=f"{int(val)}")
    scale_slider = ctk.CTkSlider(
        scale_group,
        from_=100,
        to=1000,
        width=220,
        number_of_steps=9,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_scale,
    )
    scale_slider.grid(row=1, column=1, sticky="ew", padx=0, pady=(4, 8))
    scale_slider.set(100)

    # 4. Noise Detail Group
    detail_group = ctk.CTkFrame(frame_noise_card, fg_color="transparent", corner_radius=10)
    detail_group.grid(row=3, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 16))
    detail_group.grid_columnconfigure(0, weight=0)
    detail_group.grid_columnconfigure(1, weight=1)
    detail_group.grid_columnconfigure(2, weight=0)
    ctk.CTkLabel(detail_group, text="Noise Detail", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(8, 4))
    # Octaves
    octaves_label = ctk.CTkLabel(detail_group, text="Octaves", font=ctk.CTkFont(size=13), anchor="e")
    octaves_label.grid(row=1, column=0, sticky="e", padx=(16, 8), pady=4)
    octaves_value = ctk.CTkLabel(detail_group, text="5", font=ctk.CTkFont(size=13), width=32, anchor="w")
    octaves_value.grid(row=1, column=2, sticky="w", padx=(8, 16), pady=4)
    def update_octaves(val):
        octaves_value.configure(text=f"{int(val)}")
    octaves_slider = ctk.CTkSlider(
        detail_group,
        from_=1,
        to=10,
        width=220,
        number_of_steps=9,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_octaves,
    )
    octaves_slider.grid(row=1, column=1, sticky="ew", padx=0, pady=4)
    octaves_slider.set(5)
    # Persistence
    persistence_label = ctk.CTkLabel(detail_group, text="Persistence", font=ctk.CTkFont(size=13), anchor="e")
    persistence_label.grid(row=2, column=0, sticky="e", padx=(16, 8), pady=4)
    persistence_value = ctk.CTkLabel(detail_group, text="5", font=ctk.CTkFont(size=13), width=32, anchor="w")
    persistence_value.grid(row=2, column=2, sticky="w", padx=(8, 16), pady=4)
    def update_persistence(val):
        persistence_value.configure(text=f"{int(val)}")
    persistence_slider = ctk.CTkSlider(
        detail_group,
        from_=1,
        to=10,
        width=220,
        number_of_steps=9,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_persistence,
    )
    persistence_slider.grid(row=2, column=1, sticky="ew", padx=0, pady=4)
    persistence_slider.set(5)
    # Lacunarity
    lacunarity_label = ctk.CTkLabel(detail_group, text="Lacunarity", font=ctk.CTkFont(size=13), anchor="e")
    lacunarity_label.grid(row=3, column=0, sticky="e", padx=(16, 8), pady=(4, 12))
    lacunarity_value = ctk.CTkLabel(detail_group, text="5", font=ctk.CTkFont(size=13), width=32, anchor="w")
    lacunarity_value.grid(row=3, column=2, sticky="w", padx=(8, 16), pady=(4, 12))
    def update_lacunarity(val):
        lacunarity_value.configure(text=f"{int(val)}")
    lacunarity_slider = ctk.CTkSlider(
        detail_group,
        from_=1,
        to=10,
        width=220,
        number_of_steps=9,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_lacunarity,
    )
    lacunarity_slider.grid(row=3, column=1, sticky="ew", padx=0, pady=(4, 12))
    lacunarity_slider.set(5)

    ############################################################################################################

    # Terrain Card
    frame_terrain_card = ctk.CTkFrame(
        tabview.tab("Terrain"),
        fg_color="#ffffff",
        corner_radius=14,
        border_width=1,
        border_color="#e0e6ed"
    )
    frame_terrain_card.grid(row=1, column=0, padx=8, pady=8, sticky="nsew")
    frame_terrain_card.columnconfigure(1, weight=1)

    # Terrain Tab: group parameters into two groups
    # Section header for first group
    ctk.CTkLabel(frame_terrain_card, text="Mesh Resolution", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4e84ae").grid(row=0, column=0, columnspan=3, sticky="w", padx=8, pady=(16, 0))
    # 1. Group: Resolution Factor and Base Elevation
    terrain_group1 = ctk.CTkFrame(frame_terrain_card, fg_color="transparent", corner_radius=10)
    terrain_group1.grid(row=1, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 0))
    terrain_group1.grid_columnconfigure(0, weight=0)
    terrain_group1.grid_columnconfigure(1, weight=1)
    terrain_group1.grid_columnconfigure(2, weight=0)
    # Resolution Factor
    resolution_factor_label = ctk.CTkLabel(terrain_group1, text="Resolution Factor", font=ctk.CTkFont(size=13), anchor="e")
    resolution_factor_label.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=8)
    resolution_factor_value = ctk.CTkLabel(terrain_group1, text="10", font=ctk.CTkFont(size=13), width=32, anchor="w")
    resolution_factor_value.grid(row=0, column=2, sticky="w", padx=(8, 16), pady=8)
    def update_resolution_factor(val):
        resolution_factor_value.configure(text=f"{int(val)}")
    resolution_factor_slider = ctk.CTkSlider(
        terrain_group1,
        from_=1,
        to=20,
        width=220,
        number_of_steps=20,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_resolution_factor,
    )
    resolution_factor_slider.grid(row=0, column=1, sticky="ew", padx=0, pady=8)
    resolution_factor_slider.set(10)
    # Base Elevation
    base_elevation_label = ctk.CTkLabel(terrain_group1, text="Base Elevation", font=ctk.CTkFont(size=13), anchor="e")
    base_elevation_label.grid(row=1, column=0, sticky="w", padx=(16, 8), pady=8)
    base_elevation_value = ctk.CTkLabel(terrain_group1, text="200", font=ctk.CTkFont(size=13), width=32, anchor="w")
    base_elevation_value.grid(row=1, column=2, sticky="w", padx=(8, 16), pady=8)
    def update_base_elevation(val):
        base_elevation_value.configure(text=f"{int(val)}")
    base_elevation_slider = ctk.CTkSlider(
        terrain_group1,
        from_=0,
        to=500,
        width=220,
        number_of_steps=100,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_base_elevation,
    )
    base_elevation_slider.grid(row=1, column=1, sticky="ew", padx=0, pady=8)
    base_elevation_slider.set(200)

    # Section header for second group
    ctk.CTkLabel(frame_terrain_card, text="Height Range", font=ctk.CTkFont(size=12, weight="bold"), text_color="#4e84ae").grid(row=2, column=0, columnspan=3, sticky="w", padx=8, pady=(16, 0))
    # 2. Group: Min Height and Max Height
    terrain_group2 = ctk.CTkFrame(frame_terrain_card, fg_color="transparent", corner_radius=10)
    terrain_group2.grid(row=3, column=0, columnspan=3, sticky="ew", padx=8, pady=(0, 16))
    terrain_group2.grid_columnconfigure(0, weight=0)
    terrain_group2.grid_columnconfigure(1, weight=1)
    terrain_group2.grid_columnconfigure(2, weight=0)
    # Min Height
    min_height_label = ctk.CTkLabel(terrain_group2, text="Min Height", font=ctk.CTkFont(size=13), anchor="e")
    min_height_label.grid(row=0, column=0, sticky="w", padx=(16, 8), pady=8)
    min_height_value = ctk.CTkLabel(terrain_group2, text="100", font=ctk.CTkFont(size=13), width=32, anchor="w")
    min_height_value.grid(row=0, column=2, sticky="w", padx=(8, 16), pady=8)
    def update_min_height(val):
        min_height_value.configure(text=f"{int(val)}")
    min_height_slider = ctk.CTkSlider(
        terrain_group2,
        from_=0,
        to=500,
        width=220,
        number_of_steps=100,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_min_height,
    )
    min_height_slider.grid(row=0, column=1, sticky="ew", padx=0, pady=8)
    min_height_slider.set(100)
    # Max Height
    max_height_label = ctk.CTkLabel(terrain_group2, text="Max Height", font=ctk.CTkFont(size=13), anchor="e")
    max_height_label.grid(row=1, column=0, sticky="w", padx=(16, 8), pady=8)
    max_height_value = ctk.CTkLabel(terrain_group2, text="300", font=ctk.CTkFont(size=13), width=32, anchor="w")
    max_height_value.grid(row=1, column=2, sticky="w", padx=(8, 16), pady=8)
    def update_max_height(val):
        max_height_value.configure(text=f"{int(val)}")
    max_height_slider = ctk.CTkSlider(
        terrain_group2,
        from_=0,
        to=500,
        width=220,
        number_of_steps=100,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=update_max_height,
    )
    max_height_slider.grid(row=1, column=1, sticky="ew", padx=0, pady=8)
    max_height_slider.set(300)

    ############################################################################################################

    # GENERATE MESH BUTTON
    genmesh_button = ctk.CTkButton(
        left_section,
        text="Generate Mesh",
        width=200,
        height=40,
        fg_color="#4e84ae",
        hover_color="#62a5d9",
        font=ctk.CTkFont(size=13, weight="bold"),
        command=generate_noise
    )
    genmesh_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), sticky="s")
    left_section.rowconfigure(2, weight=1)
    root.mainloop()
    
splash_root.after(1000, main_window)
splash_root.mainloop()
