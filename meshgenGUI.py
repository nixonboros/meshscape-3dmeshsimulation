import customtkinter as ctk
import json
from tkinter import filedialog
import os


def update_slider_label(label, text, value):
    label.configure(text=f"{text}: {int(value)}")


def toggle_visibility(
    switch_type, switch_variable, slider, slider_label, edit_button, frame
):
    if switch_variable.get() == "on":
        slider_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        slider.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        edit_button.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="e")
        frame.configure(fg_color="#d1d1d1")
    else:
        slider.grid_forget()
        slider_label.grid_forget()
        edit_button.grid_forget()
        frame.configure(fg_color="#dfe1e1")


def toggle_trees_visibility(*args):
    toggle_visibility(
        "trees",
        add_trees_switch,
        trees_slider,
        trees_slider_label,
        trees_edit_button,
        frame_trees,
    )


def toggle_rocks_visibility(*args):
    toggle_visibility(
        "rocks",
        add_rocks_switch,
        rocks_slider,
        rocks_slider_label,
        rocks_edit_button,
        frame_rocks,
    )


def toggle_sticks_visibility(*args):
    toggle_visibility(
        "sticks",
        add_sticks_switch,
        sticks_slider,
        sticks_slider_label,
        sticks_edit_button,
        frame_sticks,
    )


def toggle_logs_visibility(*args):
    toggle_visibility(
        "logs",
        add_logs_switch,
        logs_slider,
        logs_slider_label,
        logs_edit_button,
        frame_logs,
    )


def toggle_bushes_visibility(*args):
    toggle_visibility(
        "bushes",
        add_bushes_switch,
        bushes_slider,
        bushes_slider_label,
        bushes_edit_button,
        frame_bushes,
    )


def toggle_boulders_visibility(*args):
    toggle_visibility(
        "boulders",
        add_boulders_switch,
        boulders_slider,
        boulders_slider_label,
        boulders_edit_button,
        frame_boulders,
    )


def toggle_volcanos_visibility(*args):
    toggle_visibility(
        "volcano",
        add_volcano_switch,
        volcano_slider,
        volcano_slider_label,
        volcano_edit_button,
        frame_volcanos,
    )


def toggle_mushrooms_visibility(*args):
    toggle_visibility(
        "mushroom",
        add_mushroom_switch,
        mushroom_slider,
        mushroom_slider_label,
        mushroom_edit_button,
        frame_mushrooms,
    )


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
        "smoothness": smoothness_slider.get(),
        "minVerticesX": minVerticesX_slider.get(),
        "maxVerticesX": maxVerticesX_slider.get(),
        "minVerticesY": minVerticesY_slider.get(),
        "maxVerticesY": maxVerticesY_slider.get(),
        "add_trees": add_trees_switch.get(),
        "trees_density": trees_slider.get(),
        "add_rocks": add_rocks_switch.get(),
        "rocks_density": rocks_slider.get(),
        "add_sticks": add_sticks_switch.get(),
        "sticks_density": sticks_slider.get(),
        "add_logs": add_logs_switch.get(),
        "logs_density": logs_slider.get(),
        "add_bushes": add_bushes_switch.get(),
        "bushes_density": bushes_slider.get(),
        "add_boulders": add_boulders_switch.get(),
        "boulders_density": boulders_slider.get(),
        "add_volcano": add_volcano_switch.get(),
        "volcano_density": volcano_slider.get(),
        "add_mushroom": add_mushroom_switch.get(),
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
        smoothness_slider.set(preset_data["smoothness"])
        minVerticesX_slider.set(preset_data["minVerticesX"])
        maxVerticesX_slider.set(preset_data["maxVerticesX"])
        minVerticesY_slider.set(preset_data["minVerticesY"])
        maxVerticesY_slider.set(preset_data["maxVerticesY"])
        add_trees_switch.set(preset_data["add_trees"])
        trees_slider.set(preset_data["trees_density"])
        add_rocks_switch.set(preset_data["add_rocks"])
        rocks_slider.set(preset_data["rocks_density"])
        add_sticks_switch.set(preset_data["add_sticks"])
        sticks_slider.set(preset_data["sticks_density"])
        add_logs_switch.set(preset_data["add_logs"])
        logs_slider.set(preset_data["logs_density"])
        add_bushes_switch.set(preset_data["add_bushes"])
        bushes_slider.set(preset_data["bushes_density"])
        add_boulders_switch.set(preset_data["add_boulders"])
        boulders_slider.set(preset_data["boulders_density"])
        add_volcano_switch.set(preset_data["add_volcano"])
        volcano_slider.set(preset_data["volcano_density"])
        add_mushroom_switch.set(preset_data["add_mushroom"])
        mushroom_slider.set(preset_data["mushroom_density"])
        # Update the option menu
        preset_name = os.path.basename(file_path)[:-5]
        presets_optionmenu.configure(
            values=presets_optionmenu.cget("values") + [preset_name]
        )
        presets_optionmenu.set(preset_name)


def trees_advanced_settings_window():
    def save_trees_settings():
        trees_advanced_settings_window.destroy()

    trees_advanced_settings_window = ctk.CTkToplevel(root)
    trees_advanced_settings_window.title("Advanced Tree Settings")
    trees_advanced_settings_window.geometry("450x300")
    trees_advanced_settings_window.grab_set()

    # add tree advanced settings here

    # SAVE BUTTON FOR ADVANCED TREES SETTINGS
    save_button = ctk.CTkButton(
        trees_advanced_settings_window,
        text="Save Settings",
        command=save_trees_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    trees_advanced_settings_window.rowconfigure(4, weight=1)
    trees_advanced_settings_window.columnconfigure(0, weight=1)


def rocks_advanced_settings_window():
    def save_rocks_settings():
        # add saving function
        rocks_advanced_settings_window.destroy()

    rocks_advanced_settings_window = ctk.CTkToplevel(root)
    rocks_advanced_settings_window.title("Advanced Rock Settings")
    rocks_advanced_settings_window.geometry("450x300")
    rocks_advanced_settings_window.grab_set()

    # add rocks advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        rocks_advanced_settings_window,
        text="Save Settings",
        command=save_rocks_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    rocks_advanced_settings_window.rowconfigure(4, weight=1)
    rocks_advanced_settings_window.columnconfigure(0, weight=1)


def sticks_advanced_settings_window():
    def save_sticks_settings():
        # add saving function
        sticks_advanced_settings_window.destroy()

    sticks_advanced_settings_window = ctk.CTkToplevel(root)
    sticks_advanced_settings_window.title("Advanced Stick Settings")
    sticks_advanced_settings_window.geometry("450x300")
    sticks_advanced_settings_window.grab_set()

    # add stick advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        sticks_advanced_settings_window,
        text="Save Settings",
        command=save_sticks_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    sticks_advanced_settings_window.rowconfigure(4, weight=1)
    sticks_advanced_settings_window.columnconfigure(0, weight=1)


def logs_advanced_settings_window():
    def save_logs_settings():
        # add saving function
        logs_advanced_settings_window.destroy()

    logs_advanced_settings_window = ctk.CTkToplevel(root)
    logs_advanced_settings_window.title("Advanced Log Settings")
    logs_advanced_settings_window.geometry("450x300")
    logs_advanced_settings_window.grab_set()

    # add log advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        logs_advanced_settings_window,
        text="Save Settings",
        command=save_logs_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    logs_advanced_settings_window.rowconfigure(4, weight=1)
    logs_advanced_settings_window.columnconfigure(0, weight=1)


def bushes_advanced_settings_window():
    def save_bushes_settings():
        # add saving function
        bushes_advanced_settings_window.destroy()

    bushes_advanced_settings_window = ctk.CTkToplevel(root)
    bushes_advanced_settings_window.title("Advanced Bush Settings")
    bushes_advanced_settings_window.geometry("450x300")
    bushes_advanced_settings_window.grab_set()

    # add bush advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        bushes_advanced_settings_window,
        text="Save Settings",
        command=save_bushes_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    bushes_advanced_settings_window.rowconfigure(4, weight=1)
    bushes_advanced_settings_window.columnconfigure(0, weight=1)


############################################################################################################


def boulders_advanced_settings_window():
    def save_boulders_settings():
        # add saving function
        boulders_advanced_settings_window.destroy()

    boulders_advanced_settings_window = ctk.CTkToplevel(root)
    boulders_advanced_settings_window.title("Advanced Boulder Settings")
    boulders_advanced_settings_window.geometry("450x300")
    boulders_advanced_settings_window.grab_set()

    # add bush advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        boulders_advanced_settings_window,
        text="Save Settings",
        command=save_boulders_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    boulders_advanced_settings_window.rowconfigure(4, weight=1)
    boulders_advanced_settings_window.columnconfigure(0, weight=1)


############################################################################################################


def volcano_advanced_settings_window():
    def save_volcano_settings():
        # add saving function
        volcano_advanced_settings_window.destroy()

    volcano_advanced_settings_window = ctk.CTkToplevel(root)
    volcano_advanced_settings_window.title("Advanced Volcano Settings")
    volcano_advanced_settings_window.geometry("450x300")
    volcano_advanced_settings_window.grab_set()

    # add volcano advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        volcano_advanced_settings_window,
        text="Save Settings",
        command=save_volcano_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    volcano_advanced_settings_window.rowconfigure(4, weight=1)
    volcano_advanced_settings_window.columnconfigure(0, weight=1)


############################################################################################################


def mushroom_advanced_settings_window():
    def save_mushroom_settings():
        # add saving function
        mushroom_advanced_settings_window.destroy()

    mushroom_advanced_settings_window = ctk.CTkToplevel(root)
    mushroom_advanced_settings_window.title("Advanced Mushroom Settings")
    mushroom_advanced_settings_window.geometry("450x300")
    mushroom_advanced_settings_window.grab_set()

    # add mushroom advanced settings here

    # SAVE BUTTON
    save_button = ctk.CTkButton(
        mushroom_advanced_settings_window,
        text="Save Settings",
        command=save_mushroom_settings,
        width=50,
        fg_color="#62a5d9",
        hover_color="#4e84ae",
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    mushroom_advanced_settings_window.rowconfigure(4, weight=1)
    mushroom_advanced_settings_window.columnconfigure(0, weight=1)


############################################################################################################

# MAIN WINDOW
root = ctk.CTk()
root.title("MeshScape")
root.geometry("1100x600")
ctk.set_appearance_mode("light")
root.columnconfigure(0, weight=1)

# Left Section
left_section = ctk.CTkFrame(root)
left_section.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
root.rowconfigure(0, weight=1)

# Set the minimum width for the left section
left_section.grid_columnconfigure(0, weight=1)

# FRAME FOR TITLE LABEL
frame_title = ctk.CTkFrame(left_section, fg_color="#62a5d9")
frame_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew")
frame_title.columnconfigure(0, weight=1)

# TITLE LABEL
title_label = ctk.CTkLabel(
    frame_title,
    text="MeshScape",
    font=ctk.CTkFont(size=24, weight="bold"),
    text_color="white",
)
title_label.grid(row=0, column=0, pady=(10, 10))

# PRESETS DROPDOWN MENU
presets_label = ctk.CTkLabel(left_section, text="Preset:")
presets_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

presets_optionmenu = ctk.CTkOptionMenu(
    left_section,
    values=["Default"],
    width=200,
    fg_color="#b9bdbd",
    button_color="#9ca2a2",
    button_hover_color="#838b8b",
)
presets_optionmenu.grid(row=1, column=0, padx=(70, 10), pady=(10, 0), sticky="w")

# SAVE PRESET BUTTON
create_preset_button = ctk.CTkButton(
    left_section,
    text="Save",
    command=save_preset,
    width=50,
    fg_color="#9ca2a2",
    hover_color="#838b8b",
)
create_preset_button.grid(row=1, column=0, padx=(285, 0), pady=(10, 0), sticky="w")

# LOAD PRESET BUTTON
load_preset_button = ctk.CTkButton(
    left_section,
    text="Load",
    command=load_preset,
    width=50,
    fg_color="#9ca2a2",
    hover_color="#838b8b",
)
load_preset_button.grid(row=1, column=0, padx=(340, 0), pady=(10, 0), sticky="w")

############################################################################################################

# TABVIEW
tabview = ctk.CTkTabview(
    left_section,
    fg_color="#f2f3f3",
    segmented_button_fg_color="#9ca2a2",
    segmented_button_selected_color="#62a5d9",
    segmented_button_selected_hover_color="#4e84ae",
    segmented_button_unselected_color="#9ca2a2",
    segmented_button_unselected_hover_color="#838b8b",
)
tabview.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10)

tabview.add("Noise")
tabview.add("Terrain")
tabview.add("Objects")

tabview.set("Noise")

tabview.tab("Noise").columnconfigure(0, weight=1)
tabview.tab("Terrain").columnconfigure(0, weight=1)
tabview.tab("Objects").columnconfigure(0, weight=1)

############################################################################################################

# Right Section
right_section = ctk.CTkFrame(root, fg_color="#dbdbdb")
right_section.grid(row=0, column=1, padx=(0, 10), pady=10, sticky="new")
right_section.columnconfigure(0, weight=1)

root.columnconfigure(1, weight=1)

# Visualisation Frame
frame_visualisation = ctk.CTkFrame(
    right_section, width=190, height=560, fg_color="white"
)
frame_visualisation.grid(row=0, column=0, pady=10, padx=10, sticky="nsew")
frame_visualisation.columnconfigure(0, weight=1)

############################################################################################################

# FRAME_BASE_OBJECTS
frame_base_objects = ctk.CTkScrollableFrame(
    tabview.tab("Objects"), height=350, fg_color="#f2f3f3"
)
frame_base_objects.grid(row=0, column=0, sticky="ew")
frame_base_objects.columnconfigure(0, weight=1)

# FRAME_TREES
frame_trees = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_trees.grid(row=0, column=0, sticky="ew")

# FRAME_ROCKS
frame_rocks = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_rocks.grid(row=1, column=0, pady=(10, 0), sticky="ew")

# FRAME_STICKS
frame_sticks = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_sticks.grid(row=2, column=0, pady=(10, 0), sticky="ew")

# FRAME_LOGS
frame_logs = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_logs.grid(row=3, column=0, pady=(10, 0), sticky="ew")

# FRAME_BUSHES
frame_bushes = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_bushes.grid(row=4, column=0, pady=(10, 0), sticky="ew")

# FRAME_BOuLDERS
frame_boulders = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_boulders.grid(row=5, column=0, pady=(10, 0), sticky="ew")

frame_volcanos = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_volcanos.grid(row=6, column=0, pady=(10, 0), sticky="ew")

frame_mushrooms = ctk.CTkFrame(
    frame_base_objects, border_width=0, fg_color="#dfe1e1", corner_radius=20
)
frame_mushrooms.grid(row=7, column=0, pady=(10, 10), sticky="ew")


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
    frame_trees, text="Density: 50", width=125, anchor="w"
)
trees_slider = ctk.CTkSlider(
    frame_trees,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(trees_slider_label, "Density", value),
)
trees_slider.set(50)

# TREE EDIT BUTTON
trees_edit_button = ctk.CTkButton(
    frame_trees,
    text="Edit",
    command=trees_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

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
    frame_rocks, text="Density: 50", width=125, anchor="w"
)
rocks_slider = ctk.CTkSlider(
    frame_rocks,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(rocks_slider_label, "Density", value),
)
rocks_slider.set(50)

# ROCK EDIT BUTTON
rocks_edit_button = ctk.CTkButton(
    frame_rocks,
    text="Edit",
    command=rocks_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

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
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(sticks_slider_label, "Density", value),
)
sticks_slider.set(50)

# STICKS EDIT BUTTON
sticks_edit_button = ctk.CTkButton(
    frame_sticks,
    text="Edit",
    command=sticks_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

############################################################################################################

# ENABLE/DISABLE ADD LOGS SWITCH
add_logs_switch = ctk.StringVar(value="off")
add_logs_switch.trace_add(
    "write", toggle_logs_visibility
)  # bind toggle_slider_visibility function to switch variable
logs_switch = ctk.CTkSwitch(
    frame_logs,
    text="Logs",
    command=toggle_logs_visibility,
    variable=add_logs_switch,
    onvalue="on",
    offvalue="off",
)
logs_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# LOGS SLIDERS
logs_slider_label = ctk.CTkLabel(frame_logs, text="Density: 50", width=125, anchor="w")
logs_slider = ctk.CTkSlider(
    frame_logs,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(logs_slider_label, "Density", value),
)
logs_slider.set(50)

# LOGS EDIT BUTTON
logs_edit_button = ctk.CTkButton(
    frame_logs,
    text="Edit",
    command=logs_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

############################################################################################################

# ENABLE/DISABLE ADD BUSHES SWITCH
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

# USHES SLIDERS
bushes_slider_label = ctk.CTkLabel(
    frame_bushes, text="Density: 50", width=125, anchor="w"
)
bushes_slider = ctk.CTkSlider(
    frame_bushes,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(bushes_slider_label, "Density", value),
)
bushes_slider.set(50)

# BUSHES EDIT BUTTON
bushes_edit_button = ctk.CTkButton(
    frame_bushes,
    text="Edit",
    command=bushes_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

############################################################################################################

# ENABLE/DISABLE ADD BOULDERS SWITCH
add_boulders_switch = ctk.StringVar(value="off")
add_boulders_switch.trace_add(
    "write", toggle_boulders_visibility
)  # bind toggle_slider_visibility function to switch variable
boulders_switch = ctk.CTkSwitch(
    frame_boulders,
    text="Boulders",
    command=toggle_boulders_visibility,
    variable=add_boulders_switch,
    onvalue="on",
    offvalue="off",
)
boulders_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# BOULDER SLIDERS
boulders_slider_label = ctk.CTkLabel(
    frame_boulders, text="Density: 50", width=125, anchor="w"
)
boulders_slider = ctk.CTkSlider(
    frame_boulders,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(boulders_slider_label, "Density", value),
)
boulders_slider.set(50)

# BOULDERS EDIT BUTTON
boulders_edit_button = ctk.CTkButton(
    frame_boulders,
    text="Edit",
    command=boulders_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

############################################################################################################

# ENABLE/DISABLE ADD VOLCANO SWITCH
add_volcano_switch = ctk.StringVar(value="off")
add_volcano_switch.trace_add(
    "write", toggle_volcanos_visibility
)  # bind toggle_slider_visibility function to switch variable
volcano_switch = ctk.CTkSwitch(
    frame_volcanos,
    text="Volcano",
    command=toggle_volcanos_visibility,
    variable=add_volcano_switch,
    onvalue="on",
    offvalue="off",
)
volcano_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# VOLCANO SLIDERS
volcano_slider_label = ctk.CTkLabel(
    frame_volcanos, text="Density: 50", width=125, anchor="w"
)
volcano_slider = ctk.CTkSlider(
    frame_volcanos,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(volcano_slider_label, "Density", value),
)
volcano_slider.set(50)

# VOLCANO EDIT BUTTON
volcano_edit_button = ctk.CTkButton(
    frame_volcanos,
    text="Edit",
    command=volcano_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

############################################################################################################

# ENABLE/DISABLE ADD MUSHROOM SWITCH
add_mushroom_switch = ctk.StringVar(value="off")
add_mushroom_switch.trace_add(
    "write", toggle_mushrooms_visibility
)  # bind toggle_slider_visibility function to switch variable
mushroom_switch = ctk.CTkSwitch(
    frame_mushrooms,
    text="Mushroom",
    command=toggle_mushrooms_visibility,
    variable=add_mushroom_switch,
    onvalue="on",
    offvalue="off",
)
mushroom_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# MUSHROOM SLIDERS
mushroom_slider_label = ctk.CTkLabel(
    frame_mushrooms, text="Density: 50", width=125, anchor="w"
)
mushroom_slider = ctk.CTkSlider(
    frame_mushrooms,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(mushroom_slider_label, "Density", value),
)
mushroom_slider.set(50)

# MUSHROOM EDIT BUTTON
mushroom_edit_button = ctk.CTkButton(
    frame_mushrooms,
    text="Edit",
    command=mushroom_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)


############################################################################################################

# FRAME_BASE_NOISE
frame_base_noise = ctk.CTkScrollableFrame(
    tabview.tab("Noise"), height=350, fg_color="#f2f3f3"
)
frame_base_noise.grid(
    row=0,
    column=0,
    sticky="ew",
)

# NOISE TYPE
noise_type_label = ctk.CTkLabel(
    frame_base_noise, width=135, text="Noise Type: ", anchor="w"
)
noise_type_label.grid(row=0, column=0, sticky="w")

noise_type_dropdown = ctk.CTkOptionMenu(
    frame_base_noise,
    values=["Perlin", "Simplex", "Value", "Cellular"],
    width=100,
    fg_color="#b9bdbd",
    button_color="#9ca2a2",
    button_hover_color="#838b8b",
)
noise_type_dropdown.grid(row=0, column=1, sticky="w", padx=(15, 0))
noise_type_dropdown.set("Perlin")

# WIDTH
width_label = ctk.CTkLabel(
    frame_base_noise, text="Mesh Width: 500", width=135, anchor="w"
)
width_label.grid(row=1, column=0, sticky="w", pady=(20, 0))

width_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=100,
    to=1000,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(width_label, "Mesh Width", value),
)
width_slider.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
width_slider.set(500)

# HEIGHT
height_label = ctk.CTkLabel(
    frame_base_noise, text="Mesh Height: 500", width=135, anchor="w"
)
height_label.grid(row=2, column=0, sticky="w")

height_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=100,
    to=1000,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(height_label, "Mesh Height", value),
)
height_slider.grid(row=2, column=1, sticky="w", padx=(10, 0))
height_slider.set(500)

# SCALE
scale_label = ctk.CTkLabel(
    frame_base_noise, text="Zoom Scale: 1", width=135, anchor="w"
)
scale_label.grid(row=3, column=0, sticky="w", pady=(20, 0))

scale_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=1,
    to=10,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(scale_label, "Zoom Scale", value),
)
scale_slider.grid(row=3, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
scale_slider.set(1)

# OCTAVES
octaves_label = ctk.CTkLabel(frame_base_noise, text="Octaves: 5", width=135, anchor="w")
octaves_label.grid(row=4, column=0, sticky="w", pady=(20, 0))

octaves_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=1,
    to=10,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(octaves_label, "Octaves", value),
)
octaves_slider.grid(row=4, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
octaves_slider.set(5)

# PERSISTENCE
persistence_label = ctk.CTkLabel(
    frame_base_noise, text="Persistence: 5", width=135, anchor="w"
)
persistence_label.grid(row=5, column=0, sticky="w")

persistence_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=1,
    to=10,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(persistence_label, "Persistence", value),
)
persistence_slider.grid(row=5, column=1, sticky="w", padx=(10, 0))
persistence_slider.set(5)

# LACUNARITY
lacunarity_label = ctk.CTkLabel(
    frame_base_noise, text="Lacunarity: 5", width=135, anchor="w"
)
lacunarity_label.grid(row=6, column=0, sticky="w")

lacunarity_slider = ctk.CTkSlider(
    frame_base_noise,
    from_=1,
    to=10,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(lacunarity_label, "Lacunarity", value),
)
lacunarity_slider.grid(row=6, column=1, sticky="w", padx=(10, 0))
lacunarity_slider.set(5)

############################################################################################################

# FRAME_BASE_TERRAIN
frame_base_terrain = ctk.CTkScrollableFrame(
    tabview.tab("Terrain"), height=350, fg_color="#f2f3f3"
)
frame_base_terrain.grid(
    row=0,
    column=0,
    sticky="ew",
)

# RESOLUTION FACTOR
resolution_factor_label = ctk.CTkLabel(
    frame_base_terrain, text="Resolution Factor: 5", width=135, anchor="w"
)
resolution_factor_label.grid(row=0, column=0, sticky="w")

resolution_factor_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=1,
    to=10,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        resolution_factor_label, "Resolution Factor", value
    ),
)
resolution_factor_slider.grid(row=0, column=1, sticky="w", padx=(10, 0))
resolution_factor_slider.set(5)

# BASE ELEVATION
base_elevation_label = ctk.CTkLabel(
    frame_base_terrain, text="Base Elevation: 50", width=135, anchor="w"
)
base_elevation_label.grid(row=1, column=0, sticky="w", pady=(20, 0))

base_elevation_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=0,
    to=100,
    width=400,
    number_of_steps=100,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        base_elevation_label, "Base Elevation", value
    ),
)
base_elevation_slider.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
base_elevation_slider.set(50)

# MIN HEIGHT
min_height_label = ctk.CTkLabel(
    frame_base_terrain, text="Min  Height: 500", width=135, anchor="w"
)
min_height_label.grid(row=2, column=0, sticky="w", pady=(20, 0))

min_height_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=1000,
    width=400,
    number_of_steps=99,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(min_height_label, "Min  Height", value),
)
min_height_slider.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
min_height_slider.set(500)

# MAX HEIGHT
max_height_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Height: 500", width=135, anchor="w"
)
max_height_label.grid(row=3, column=0, sticky="w")

max_height_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=1000,
    width=400,
    number_of_steps=99,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(max_height_label, "Max Height", value),
)
max_height_slider.grid(row=3, column=1, sticky="w", padx=(10, 0))
max_height_slider.set(500)


# SMOOTHNESS
smoothness_label = ctk.CTkLabel(
    frame_base_terrain, text="Smoothness: 5", width=135, anchor="w"
)
smoothness_label.grid(row=4, column=0, sticky="w", pady=(20, 0))

smoothness_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=0,
    to=10,
    width=400,
    number_of_steps=10,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(smoothness_label, "Smoothness", value),
)
smoothness_slider.grid(row=4, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
smoothness_slider.set(5)

# MIN VERTICES X
minVerticesX_label = ctk.CTkLabel(
    frame_base_terrain, text="Min  Vertices X: 50", width=135, anchor="w"
)
minVerticesX_label.grid(row=5, column=0, sticky="w", pady=(20, 0))

minVerticesX_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        minVerticesX_label, "Min  Vertices X", value
    ),
)
minVerticesX_slider.grid(row=5, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
minVerticesX_slider.set(50)

# MAX VERTICES X
maxVerticesX_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Vertices X: 10", width=135, anchor="w"
)
maxVerticesX_label.grid(
    row=6,
    column=0,
    sticky="w",
)

maxVerticesX_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        maxVerticesX_label, "Max Vertices X", value
    ),
)
maxVerticesX_slider.grid(row=6, column=1, sticky="w", padx=(10, 0))
maxVerticesX_slider.set(50)

# MIN VERTICES Y
minVerticesY_label = ctk.CTkLabel(
    frame_base_terrain, text="Min  Vertices Y: 50", width=135, anchor="w"
)
minVerticesY_label.grid(row=7, column=0, sticky="w", pady=(20, 0))

minVerticesY_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=5,
    to=100,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        minVerticesY_label, "Min  Vertices Y", value
    ),
)
minVerticesY_slider.grid(row=7, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
minVerticesY_slider.set(50)

# MAX VERTICES Y
maxVerticesY_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Vertices Y: 50", width=135, anchor="w"
)
maxVerticesY_label.grid(row=8, column=0, sticky="w")

maxVerticesY_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    number_of_steps=9,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        maxVerticesY_label, "Max Vertices Y", value
    ),
)
maxVerticesY_slider.grid(row=8, column=1, sticky="w", padx=(10, 0))
maxVerticesY_slider.set(50)

############################################################################################################


# OBJECT FRAME CLICKABLE
def bind_toggle_switch_and_cursor(frame, switch_variable, toggle_function):
    def toggle_frame_switch(event):
        # Toggle the switch value when the frame is clicked
        if switch_variable.get() == "on":
            switch_variable.set("off")
        else:
            switch_variable.set("on")
        toggle_function()

    frame.bind("<Button-1>", toggle_frame_switch)
    frame.configure(cursor="hand2")


bind_toggle_switch_and_cursor(frame_trees, add_trees_switch, toggle_trees_visibility)
bind_toggle_switch_and_cursor(frame_rocks, add_rocks_switch, toggle_rocks_visibility)
bind_toggle_switch_and_cursor(frame_sticks, add_sticks_switch, toggle_sticks_visibility)
bind_toggle_switch_and_cursor(frame_logs, add_logs_switch, toggle_logs_visibility)
bind_toggle_switch_and_cursor(frame_bushes, add_bushes_switch, toggle_bushes_visibility)
bind_toggle_switch_and_cursor(
    frame_boulders, add_boulders_switch, toggle_boulders_visibility
)
bind_toggle_switch_and_cursor(
    frame_volcanos, add_volcano_switch, toggle_volcanos_visibility
)
bind_toggle_switch_and_cursor(
    frame_mushrooms, add_mushroom_switch, toggle_mushrooms_visibility
)

############################################################################################################

# GENERATE MESH BUTTON
genmesh_button = ctk.CTkButton(
    left_section,
    text="Generate Mesh",
    width=200,
    height=40,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)
genmesh_button.grid(row=3, column=0, columnspan=2, pady=(10, 10), sticky="s")
left_section.rowconfigure(2, weight=1)

root.mainloop()
