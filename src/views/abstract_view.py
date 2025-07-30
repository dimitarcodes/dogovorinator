from src.logger import DogovLogger
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from abc import ABC, abstractmethod

class AbstractView(ABC):
    def __init__(self, root :  tk.Tk, controller):

        self.main_frame = ttk.Frame(root, padding = 10)
        self._controller = controller
        
        self._init_logic()
        self._build_gui()
        self.hide()
    
    # @abstractmethod
    def _init_logic(self):
        # get necessary data from controller
        pass

    @abstractmethod
    def _build_gui(self):
        # build GUI elements (widgets)
        pass

    def show(self):
        self.main_frame.pack(fill=tk.BOTH, expand=True)
    
    def hide(self):
        self.main_frame.pack_forget()

    @property
    def controller(self):
        """The controller responsible for communicating with model layer and managing views."""
        return self._controller
    
    @controller.setter
    def controller(self, ctrlr):
        self._controller = ctrlr