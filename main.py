
import tkinter
from tkinter import ttk
from src.controller import AppController
from src.model import DogovorinatorModel
from src.db import DogovorinatorDatabase

from src.logger import DogovLogger
import sv_ttk

def main():
    app = AppController()
    app.run()

if __name__ == "__main__":
    main()