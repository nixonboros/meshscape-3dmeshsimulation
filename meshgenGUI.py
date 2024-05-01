import customtkinter as ctk


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


def create_new_preset():
    dialog = ctk.CTkInputDialog(
        text="Enter the name of the new preset:", title="Create New Preset"
    )  # modal dialog for preset creation
    preset_name = dialog.get_input()
    if preset_name:
        current_values = presets_optionmenu.cget("values")
        current_values.append(preset_name)
        presets_optionmenu.configure(values=current_values)
        presets_optionmenu.set(preset_name)


def delete_preset():
    selected_preset = presets_optionmenu.get()
    if selected_preset != "None":
        current_values = presets_optionmenu.cget("values")
        current_values.remove(selected_preset)
        presets_optionmenu.configure(values=current_values)
        presets_optionmenu.set("None")


def trees_advanced_settings_window():
    def save_trees_settings():
        trees_advanced_settings_window.destroy()

    trees_advanced_settings_window = ctk.CTkToplevel(root)
    trees_advanced_settings_window.title("Advanced Tree Settings")
    trees_advanced_settings_window.geometry("450x300")
    trees_advanced_settings_window.grab_set()

    # EXAMPLE DROPDOWN FOR TREES SHAPE
    shape_label = ctk.CTkLabel(
        trees_advanced_settings_window, text="Tree Shape:", width=100, anchor="w"
    )
    shape_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    shape_optionmenu = ctk.CTkOptionMenu(
        trees_advanced_settings_window,
        values=["Mixed", "Spherical", "Conical"],
        width=260,
        fg_color="#a8adad",
        button_color="#838b8b",
        button_hover_color="#5b6161",
    )
    shape_optionmenu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # EXAMPLE LABELS FOR ADVANCED TREES SETTINGS
    density_label = ctk.CTkLabel(
        trees_advanced_settings_window, text="Trees Density: 50", width=100, anchor="w"
    )
    density_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

    trunk_width_label = ctk.CTkLabel(
        trees_advanced_settings_window, text="Trunk Width: 50", width=100, anchor="w"
    )
    trunk_width_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    leaf_size_label = ctk.CTkLabel(
        trees_advanced_settings_window, text="Leaf Size: 50", width=100, anchor="w"
    )
    leaf_size_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # EXAMPLE SLIDERS FOR ADVANCED TREES SETTINGS
    density_slider = ctk.CTkSlider(
        trees_advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(
            density_label, "Trees Density", value
        ),
    )
    density_slider.grid(row=1, column=1, padx=10, pady=10, sticky="e")

    trunk_width_slider = ctk.CTkSlider(
        trees_advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(
            trunk_width_label, "Trunk Width", value
        ),
    )
    trunk_width_slider.grid(row=2, column=1, padx=10, pady=10, sticky="e")

    leaf_size_slider = ctk.CTkSlider(
        trees_advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        button_color="#62a5d9",
        button_hover_color="#4e84ae",
        command=lambda value: update_slider_label(leaf_size_label, "Leaf Size", value),
    )
    leaf_size_slider.grid(row=3, column=1, padx=10, pady=10, sticky="e")

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
    font=ctk.CTkFont(size=24),
    text_color="white",
)
title_label.grid(row=0, column=0, pady=(10, 10))

# PRESETS DROPDOWN MENU
presets_label = ctk.CTkLabel(left_section, text="Preset:")
presets_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

presets_optionmenu = ctk.CTkOptionMenu(
    left_section,
    values=["None"],
    width=200,
    fg_color="#b9bdbd",
    button_color="#9ca2a2",
    button_hover_color="#838b8b",
    text_color="#323434",
)
presets_optionmenu.grid(row=1, column=0, padx=(70, 10), pady=(10, 0), sticky="w")

# CREATE PRESET BUTTON
create_preset_button = ctk.CTkButton(
    left_section,
    text="+",
    command=create_new_preset,
    width=30,
    fg_color="#9ca2a2",
    hover_color="#838b8b",
    text_color="#323434",
)
create_preset_button.grid(row=1, column=0, padx=(285, 0), pady=(10, 0), sticky="w")

# DELETE PRESET BUTTON
delete_preset_button = ctk.CTkButton(
    left_section,
    text="-",
    command=delete_preset,  # adding delelte confirmation window
    width=30,
    fg_color="#9ca2a2",
    hover_color="#838b8b",
    text_color="#323434",
)
delete_preset_button.grid(row=1, column=0, padx=(320, 0), pady=(10, 0), sticky="w")

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
frame_boulders.grid(row=5, column=0, pady=(10, 10), sticky="ew")

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
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        sticks_slider_label, "Density", value
    ),
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
logs_slider_label = ctk.CTkLabel(
    frame_logs, text="Density: 50", width=125, anchor="w"
)
logs_slider = ctk.CTkSlider(
    frame_logs,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        logs_slider_label, "Density", value
    ),
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
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        bushes_slider_label, "Density", value
    ),
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

# USHES SLIDERS
boulders_slider_label = ctk.CTkLabel(
    frame_boulders, text="Density: 50", width=125, anchor="w"
)
boulders_slider = ctk.CTkSlider(
    frame_boulders,
    from_=0,
    to=100,
    width=330,  # make scalable to window
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        boulders_slider_label, "Density", value
    ),
)
boulders_slider.set(50)

# boulders EDIT BUTTON
boulders_edit_button = ctk.CTkButton(
    frame_boulders,
    text="Edit",
    command=boulders_advanced_settings_window,
    width=50,
    fg_color="#62a5d9",
    hover_color="#4e84ae",
)

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

# SIZE X
sizeX_label = ctk.CTkLabel(frame_base_terrain, text="Size X: 10", width=120, anchor="w")
sizeX_label.grid(row=0, column=0, sticky="w")

sizeX_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(sizeX_label, "Size X", value),
)
sizeX_slider.grid(row=0, column=1, sticky="w", padx=(10, 0))
sizeX_slider.set(10)

# SIZE Y
SizeY_label = ctk.CTkLabel(frame_base_terrain, text="Size Y: 10", width=120, anchor="w")
SizeY_label.grid(row=1, column=0, sticky="w")

SizeY_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(SizeY_label, "Size Y", value),
)
SizeY_slider.grid(row=1, column=1, sticky="w", padx=(10, 0))
SizeY_slider.set(10)

# MIN VERTICES X
minVerticesX_label = ctk.CTkLabel(
    frame_base_terrain, text="Min  Vertices X: 5", width=120, anchor="w"
)
minVerticesX_label.grid(row=2, column=0, sticky="w", pady=(20, 0))

minVerticesX_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=5,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        minVerticesX_label, "Min  Vertices X", value
    ),
)
minVerticesX_slider.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
minVerticesX_slider.set(5)

# MAX VERTICES X
maxVerticesX_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Vertices X: 10", width=120, anchor="w"
)
maxVerticesX_label.grid(
    row=3,
    column=0,
    sticky="w",
)

maxVerticesX_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        maxVerticesX_label, "Max Vertices X", value
    ),
)
maxVerticesX_slider.grid(row=3, column=1, sticky="w", padx=(10, 0))
maxVerticesX_slider.set(10)

# MIN VERTICES Y
minVerticesY_label = ctk.CTkLabel(
    frame_base_terrain, text="Min  Vertices Y: 5", width=120, anchor="w"
)
minVerticesY_label.grid(row=4, column=0, sticky="w", pady=(20, 0))

minVerticesY_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=5,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        minVerticesY_label, "Min  Vertices Y", value
    ),
)
minVerticesY_slider.grid(row=4, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
minVerticesY_slider.set(5)

# MAX VERTICES Y
maxVerticesY_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Vertices Y: 10", width=120, anchor="w"
)
maxVerticesY_label.grid(row=5, column=0, sticky="w")

maxVerticesY_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=10,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(
        maxVerticesY_label, "Max Vertices Y", value
    ),
)
maxVerticesY_slider.grid(row=5, column=1, sticky="w", padx=(10, 0))
maxVerticesY_slider.set(10)

# MAX HEIGHT
maxHeight_label = ctk.CTkLabel(
    frame_base_terrain, text="Max Height: 1", width=120, anchor="w"
)
maxHeight_label.grid(row=6, column=0, sticky="w", pady=(20, 0))

maxHeight_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=1,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(maxHeight_label, "Max Height", value),
)
maxHeight_slider.grid(row=6, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
maxHeight_slider.set(1)

# SMOOTHNESS
smoothness_label = ctk.CTkLabel(
    frame_base_terrain, text="Smoothness: 1", width=120, anchor="w"
)
smoothness_label.grid(row=7, column=0, sticky="w", pady=(20, 0))

smoothness_slider = ctk.CTkSlider(
    frame_base_terrain,
    from_=1,
    to=100,
    width=400,
    button_color="#62a5d9",
    button_hover_color="#4e84ae",
    command=lambda value: update_slider_label(smoothness_label, "Smoothness", value),
)
smoothness_slider.grid(row=7, column=1, sticky="w", padx=(10, 0), pady=(20, 0))
smoothness_slider.set(1)


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
bind_toggle_switch_and_cursor(
    frame_logs, add_logs_switch, toggle_logs_visibility
)
bind_toggle_switch_and_cursor(frame_bushes, add_bushes_switch, toggle_bushes_visibility)
bind_toggle_switch_and_cursor(frame_boulders, add_boulders_switch, toggle_boulders_visibility)

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
