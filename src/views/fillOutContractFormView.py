
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from tkcalendar import DateEntry

class filloutContractFormView:
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Попълнете нужните данни")
        
        # Form frame
        self.employee_details_frame = ttk.LabelFrame(self.main_frame, text="Данни за служителя", padding="10")
        
        self.employee_details_frame_list = []

        fields = [
            "Име на служителя",
            "ID на служителя",
            "Длъжност",
            "Дата на започване",
            "Дата на приключване"
        ]
        colors = [
            "lightblue", "lightgreen", "lightyellow", "lightcoral", "lightcyan"
        ]

        for i, field in enumerate(fields):

            label = ttk.LabelFrame(self.employee_details_frame, text=f"{field}", padding="5")
            if "Дата" in field:
                entry = DateEntry(label, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern="dd-mm-yyyy")
            else:
                entry = ttk.Entry(label)
            # label.pack(anchor="w")
            self.employee_details_frame_list.append((label, entry))
        
        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        # self.back_button = ttk.Button(self.nav_frame, text="Назад" ) #, command=self.go_back)
        # self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.go_to_start)
        self.next_button = ttk.Button(self.nav_frame, text="Напред", command=self.go_next, padding="5") 

        self.hide()

    def collect_employee_data(self):
        employee_data = {}
        for label, entry in self.employee_details_frame_list:
            field_name = label.cget("text")
            employee_data[field_name] = entry.get()
        return employee_data
    
    def go_next(self):
        self.controller.set_employee_data(self.collect_employee_data())
        self.controller.next_step()

    def set_controller(self, controller):
        self.controller = controller

    def show(self):

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))
        self.employee_details_frame.pack(fill=tk.BOTH, pady=(0, 20))
        for label, entry in self.employee_details_frame_list:
            label.pack(fill=tk.X)
            entry.pack(fill=tk.X, pady=(0, 10))
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")
        self.next_button.pack(side="right", padx=(10, 0))

    def hide(self):
        # pass
        self.main_frame.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()

    # root.tk.call("source", "assets/theme/light.tcl")
    # style = ttk.Style(root)
    # # style.theme_use('light') 
    # root.tk.call("set_theme", "light")
    root.geometry("800x600")

    root.title("Fill Out Contract Form")
    app = filloutContractFormView(root)
    app.show()
    root.mainloop()