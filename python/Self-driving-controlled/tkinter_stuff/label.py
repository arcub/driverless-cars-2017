import tkinter as tk

#create a tkinter label
class Label:

    def __init__(self, controller, txt, fnt, bg_clr, rw, rwspn, clm, clmspn):

        self.new_label = tk.Label(controller, text = txt, font = fnt)
        self.new_label.configure(bg = bg_clr)
        self.new_label.grid(row = rw, rowspan = rwspn, column = clm, columnspan = clmspn)
