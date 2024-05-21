import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

class Spinner:
    def __init__(self, root, spinner_image_path="View/media/spinner.gif"):
        self.root = root
        self.spinner_image_path = spinner_image_path
        self.spinner_label = None
        self.frames = None
        self.running = False

    def show(self):
        self.spinner_label = tk.Label(self.root)
        self.spinner_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        spinner_gif = Image.open(self.spinner_image_path)
        self.frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(spinner_gif)]

        self.running = True
        self.update_spinner(0)

    def update_spinner(self, index):
        if not self.running:
            return
        frame = self.frames[index]
        index += 1
        if index >= len(self.frames):
            index = 0
        self.spinner_label.configure(image=frame)
        self.root.after(50, self.update_spinner, index)

    def hide(self):
        self.running = False
        if self.spinner_label:
            self.spinner_label.destroy()
            self.spinner_label = None
