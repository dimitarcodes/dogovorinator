
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

log = DogovLogger.get_logger()
class ReviewSubmissionsView(AbstractView):

    def _build_gui(self):
        self.label = tk.Label(self.main_frame, text="Final Page.")
        self.text_area = tk.Text(self.main_frame, height=10, width=50)
        self.label.pack(pady=(0, 20))
        self.text_area.pack(pady=(0, 20))

    def show(self):
        super().show()
        self._on_load()

    def _on_load(self):
        
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
            log.info(f"Error loading data in the submission reviewer: {e}")