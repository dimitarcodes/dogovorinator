import tkinter
from tkinter import ttk
from src.controller import AppController
from src.model import DogovorinatorModel
from src.db import DogovorinatorDatabase
import sv_ttk

def main():
    
    app = tkinter.Tk()
    sv_ttk.set_theme("light")  # Set the theme to light
    app.title("Генератор на трудови договори")
    app.geometry("800x600")

    # Initialize MVC components
    databaseController = DogovorinatorDatabase()
    model = DogovorinatorModel(databaseController)  
    controller = AppController(model, app)

    # Start the application
    app.mainloop()

if __name__ == "__main__":
    main()