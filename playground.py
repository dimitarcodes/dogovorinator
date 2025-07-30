import tkinter as tk
from tkinter import font

root = tk.Tk()
available_fonts = list(font.families())
available_fonts.sort()

# Print them out
for f in available_fonts:
    print(f)

root.destroy()
