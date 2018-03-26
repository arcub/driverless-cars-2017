import label as lbl
import tkinter as tk

class Basic(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.b1 = lbl.Label(self, "Hello", ("system", 20), "#FF1919", 0, 1, 0, 1)
