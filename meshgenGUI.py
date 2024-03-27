import customtkinter as ctk
from PIL import Image


def update_slider_label(label, text, value):
    label.configure(text=f"{text}: {int(value)}")


def toggle_slider_visibility(*args):
    # TREES SWITCH
    if add_trees_switch.get() == "on":
        trees_slider_label.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="w")
        trees_slider.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ew")
        edit_button.grid(row=1, column=2, padx=(0, 10), pady=(0, 10), sticky="e")
        frame_trees.configure(fg_color="#b8bbbb")
    else:
        trees_slider.grid_forget()
        trees_slider_label.grid_forget()
        edit_button.grid_forget()
        frame_trees.configure(fg_color="#bfc2c2")


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


def tree_advanced_settings_window():
    def save_settings():
        advanced_settings_window.destroy()

    advanced_settings_window = ctk.CTkToplevel(root)
    advanced_settings_window.title("Advanced Tree Settings")
    advanced_settings_window.geometry("400x300")
    advanced_settings_window.grab_set()

    # DROPDOWN FOR TREE SHAPE
    shape_label = ctk.CTkLabel(advanced_settings_window, text="Tree Shape:", width=100)
    shape_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    shape_optionmenu = ctk.CTkOptionMenu(
        advanced_settings_window,
        values=["Mixed", "Spherical", "Conical"],
        width=260,
        fg_color="#a8adad",
        button_color="#838b8b",
        button_hover_color="#5b6161",
    )
    shape_optionmenu.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    # LABELS FOR ADVANCED TREE SETTINGS
    density_label = ctk.CTkLabel(
        advanced_settings_window, text="Tree Density: 50", width=100
    )
    density_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    trunk_width_label = ctk.CTkLabel(
        advanced_settings_window, text="Trunk Width: 50", width=100
    )
    trunk_width_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
    leaf_size_label = ctk.CTkLabel(
        advanced_settings_window, text="Leaf Size: 50", width=100
    )
    leaf_size_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # SLIDERS FOR ADVANCED TREE SETTINGS
    density_slider = ctk.CTkSlider(
        advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        command=lambda value: update_slider_label(density_label, "Tree Density", value),
    )
    density_slider.grid(row=1, column=1, padx=10, pady=10, sticky="e")
    trunk_width_slider = ctk.CTkSlider(
        advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        command=lambda value: update_slider_label(
            trunk_width_label, "Trunk Width", value
        ),
    )
    trunk_width_slider.grid(row=2, column=1, padx=10, pady=10, sticky="e")
    leaf_size_slider = ctk.CTkSlider(
        advanced_settings_window,
        from_=0,
        to=100,
        width=260,
        command=lambda value: update_slider_label(leaf_size_label, "Leaf Size", value),
    )
    leaf_size_slider.grid(row=3, column=1, padx=10, pady=10, sticky="e")

    # SAVE BUTTON FOR ADVANCED TREE SETTINGS
    save_button = ctk.CTkButton(
        advanced_settings_window, text="Save Settings", command=save_settings, width=50
    )
    save_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="se")

    advanced_settings_window.rowconfigure(4, weight=1)
    advanced_settings_window.columnconfigure(0, weight=1)


############################################################################################################

# MAIN WINDOW
root = ctk.CTk()
root.title("3D Mesh Generation")
root.geometry("800x500")
ctk.set_appearance_mode("light")
root.columnconfigure(0, weight=1)

# FRAME FOR TITLE LABEL
frame_title = ctk.CTkFrame(root, fg_color="#3b8ed0")
frame_title.grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 20), sticky="ew")
frame_title.columnconfigure(0, weight=1)

# TITLE LABEL
title_label = ctk.CTkLabel(
    frame_title,
    text="3D Mesh Generation",
    font=ctk.CTkFont(weight="bold", size=24),
    text_color="white",
)
title_label.grid(row=0, column=0, pady=(10, 10))

# PRESETS DROPDOWN MENU
presets_label = ctk.CTkLabel(root, text="Preset:")
presets_label.grid(row=1, column=0, padx=20, pady=(10, 0), sticky="w")

presets_optionmenu = ctk.CTkOptionMenu(
    root,
    values=["None"],
    width=200,
    fg_color="#a8adad",
    button_color="#838b8b",
    button_hover_color="#5b6161",
)
presets_optionmenu.grid(row=1, column=0, padx=(70, 10), pady=(10, 0), sticky="w")

# CREATE PRESET BUTTON
create_preset_button = ctk.CTkButton(
    root,
    text="+",
    command=create_new_preset,
    width=30,
    fg_color="#838B8B",
    hover_color="#5b6161",
)
create_preset_button.grid(row=1, column=0, padx=(285, 0), pady=(10, 0), sticky="w")

# DELETE PRESET BUTTON
delete_preset_button = ctk.CTkButton(
    root,
    text="-",
    command=delete_preset, # adding delelte confirmation window 
    width=30,
    fg_color="#838B8B",
    hover_color="#5b6161",
)
delete_preset_button.grid(row=1, column=0, padx=(320, 0), pady=(10, 0), sticky="w")

############################################################################################################

# TABVIEW
tabview = ctk.CTkTabview(root)
tabview.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10)

tabview.add("Objects") 
tabview.add("Other") 

tabview.set("Objects")

tabview.tab("Objects").rowconfigure(0, weight=1)
tabview.tab("Objects").columnconfigure(0, weight=1)

# FRAME_BASE
frame_base = ctk.CTkScrollableFrame(tabview.tab("Objects"), height=350)
frame_base.grid(row=0, column=0, sticky="ew")
frame_base.columnconfigure(0, weight=1)

# FRAME_TREES
frame_trees = ctk.CTkFrame(
    frame_base, border_width=0, fg_color="#bfc2c2", corner_radius=20
)
frame_trees.grid(row=0, column=0, sticky="ew")

# FRAME_ROCKS
frame_rocks = ctk.CTkFrame(
    frame_base, border_width=0, fg_color="#bfc2c2", corner_radius=20
)
frame_rocks.grid(row=1, column=0, pady=(10, 0), sticky="ew")

# FRAME_STICKS
frame_sticks = ctk.CTkFrame(
    frame_base, border_width=0, fg_color="#bfc2c2", corner_radius=20
)
frame_sticks.grid(row=2, column=0, pady=(10, 0), sticky="ew")

# FRAME_PEBBLES
frame_pebbles = ctk.CTkFrame(
    frame_base, border_width=0, fg_color="#bfc2c2", corner_radius=20
)
frame_pebbles.grid(row=3, column=0, pady=(10, 0), sticky="ew")

# FRAME_BUSHES
frame_bushes = ctk.CTkFrame(
    frame_base, border_width=0, fg_color="#bfc2c2", corner_radius=20
)
frame_bushes.grid(row=4, column=0, pady=(10, 10), sticky="ew")

############################################################################################################

# ENABLE/DISABLE TREES SWITCH
add_trees_switch = ctk.StringVar(value="off")
add_trees_switch.trace_add(
    "write", toggle_slider_visibility
)  # bind toggle_slider_visibility function to switch variable
trees_switch = ctk.CTkSwitch(
    frame_trees,
    text="Trees",
    command=toggle_slider_visibility,
    variable=add_trees_switch,
    onvalue="on",
    offvalue="off",
)
trees_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# TREE SLIDERS
trees_slider_label = ctk.CTkLabel(frame_trees, text="Amount of Trees: 0", width=125)
trees_slider = ctk.CTkSlider(
    frame_trees,
    from_=0,
    to=100,
    width=520, # make scalable to window 
    command=lambda value: update_slider_label(
        trees_slider_label, "Amount of Trees", value
    ),
)
trees_slider.set(0)

# TREE EDIT BUTTON
edit_button = ctk.CTkButton(
    frame_trees, text="Edit", command=tree_advanced_settings_window, width=50
)

############################################################################################################

# ENABLE/DISABLE ADD ROCKS BUTTON
add_rocks_switch = ctk.StringVar(value="off")
rocks_switch = ctk.CTkSwitch(
    frame_rocks,
    text="Rocks",
    onvalue="on",
    offvalue="off",
)
rocks_switch.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# ENABLE/DISABLE ADD STICKS BUTTON
add_sticks_switch = ctk.StringVar(value="off")
sticks_switch = ctk.CTkSwitch(
    frame_sticks,
    text="Sticks",
    onvalue="on",
    offvalue="off",
)
sticks_switch.grid(row=1, column=0, padx=10, pady=10, sticky="w")

# ENABLE/DISABLE ADD PEBBLES SWITCH
add_pebbles_switch = ctk.StringVar(value="off")
pebbles_switch = ctk.CTkSwitch(
    frame_pebbles,
    text="Pebbles",
    onvalue="on",
    offvalue="off",
)
pebbles_switch.grid(row=2, column=0, padx=10, pady=10, sticky="w")

# ENABLE/DISABLE ADD BUSHES SWITCH
add_bushes_switch = ctk.StringVar(value="off")
bushes_switch = ctk.CTkSwitch(
    frame_bushes,
    text="Bushes",
    onvalue="on",
    offvalue="off",
)
bushes_switch.grid(row=3, column=0, padx=10, pady=10, sticky="w")

############################################################################################################

# GENERATE MESH BUTTON
genmesh_button = ctk.CTkButton(root, text="Generate Mesh", width=200, height=40)
genmesh_button.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="s")
root.rowconfigure(2, weight=1)

root.mainloop()