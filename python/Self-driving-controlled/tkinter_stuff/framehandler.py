import tkinter as tk
import os
from frames.basic import Basic

list_frames = [Basic]

class Main(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side = "top", fill = "both", expand = True)

        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.state = True

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.kill)

        self.frames = {}

        for f in list_frames:
            frame = f(container, self)

            self.frames[f] = frame

            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.show_frame(Basic)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def toggle_fullscreen(self, event = None):
        self.state = not self.state
        self.attributes("-fullscreen", self.state)

    def kill(self, event = None):
        print("[INFO] closing...")
        self.destroy()

app = Main()
app.title("Test")
app.mainloop()
