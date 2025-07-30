
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class StartPage:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.frame = ttk.Frame(self.root)
        self.label = ttk.Label(self.frame, text="Welcome to the Start Page")


        # button for going to next page
        self.next_button = ttk.Button(self.frame, text="Next", width=10)

        self.next_button.pack(side=tk.RIGHT, padx=5)
        self.label.pack()
        self.frame.pack()

    def set_controller(self, controller):
        self.controller = controller
        self.next_button.config(command = controller.next_step)

    def show(self):
        self.frame.pack(fill=tk.BOTH, expand=True)

    def hide(self):
        self.frame.pack_forget()


