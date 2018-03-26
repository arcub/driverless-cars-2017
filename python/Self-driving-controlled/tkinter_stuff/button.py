import tkinter as tk

#create a tkinter button
class Button:

    def __init__(self, txt, fnt, rw, rwspn, clm, clmspn, bg_clr, cmd):
        self.new_button = tk.Button(self, text = txt, font = fnt, command = cmd)
        self.new_button.configure(bg = bg_clr, relief = 'raised')
        self.new_button.grid(row = rw, rowspan = rwspn, clm = clm, columnspan = clmspn)
