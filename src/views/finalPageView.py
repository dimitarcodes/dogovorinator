
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class FinalPageView:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.frame = tk.Frame(root)
        self.label = tk.Label(self.frame, text="Final Page.")
        self.text_area = tk.Text(self.frame, height=10, width=50)
        
    def set_controller(self, controller):
        self.controller = controller
        # self.prev_button.config(command = controller.prev_step)

    def show(self):
        self.load_data()
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.label.pack(pady=(0, 20))
        self.text_area.pack(pady=(0, 20))

    def load_data(self):
        try:

            text = ""
            text += "Collected Information:\n"
            text += "Company: {}\n".format(self.controller.model.selected_company['name'])
            text += "Contract Type: {}\n".format(self.controller.model.selected_contract_type)
            text += "Employee Data:\n"
            employee_data = self.controller.model.employee_data
            for field, value in employee_data.items():
                text += "{}: {}\n".format(field, value)
            self.text_area.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")

    def hide(self):
        self.frame.pack_forget()