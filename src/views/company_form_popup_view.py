import tkinter as tk
from tkinter import ttk, messagebox
from src.models.entities import Company
from src.logger import DogovLogger
log = DogovLogger.get_logger()


class CompanyFormPopupView():

    def __init__(self, root, controller, company: Company|None = None): 
        self._root = root
        self.controller = controller
        self.company = company
        self.mode = "edit" if company else "add"
        self._build_gui()


        
        
    def _build_gui(self):
        self.popup = tk.Toplevel(self._root)
        self.popup.geometry("400x300")
        self._position_popup()

        # ensure it appears on top and main window interactions are disabled
        self.popup.transient(self._root)
        self.popup.grab_set()
        self._root.attributes("-disabled", True)
        self.popup.protocol("WM_DELETE_WINDOW", lambda: self._on_close())
        
        popup_title = "Редактиране на фирма"
        if self.mode == "add":
            popup_title = "Добавяне на фирма"
        self.popup.wm_title(popup_title)

        self.main_frame = ttk.Frame(self.popup, padding=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        # Company form
        self.company_frame = ttk.LabelFrame(self.main_frame, text="Детайли на компанията", padding=20)
        self.company_frame.pack(fill=tk.BOTH, pady=(0, 10))

        self.company_form = {}
        for field in Company.get_fields():
            
            # set the widget's name for easy access later
            label = ttk.Label(self.company_frame, text=field)
            entry = ttk.Entry(self.company_frame)
            self.company_form[field] = entry

            label.pack()
            entry.pack()

            if self.company and hasattr(self.company, field):
                entry.insert(0, getattr(self.company, field))
        

        nav_frame = ttk.Frame(self.main_frame)
        save_button = ttk.Button(nav_frame, 
                    text="Запази", 
                    command=lambda: self._save_company(self.company)
                    )      
        nav_frame.pack(fill=tk.X, pady=(10, 0))
        save_button.pack(side=tk.RIGHT, padx=(0, 10))

    def _position_popup(self):
        x = self._root.winfo_x() + (self._root.winfo_width() // 2) - 200
        y = self._root.winfo_y() + (self._root.winfo_height() // 2) - 150
        self.popup.geometry(f"+{x}+{y}")
    
    def _on_close(self):
        self._root.attributes("-disabled", False)
        self.popup.destroy()
        log.info("Company form closed without saving.")
        self.controller.destroy_company_form()

    def _validate_company_form(self):
        data = {}
        for form_field in self.company_form:
            input_value = self.company_form[form_field].get().strip()
            if not input_value:
                self._invalid_input_message(empty_input_field=form_field)
                return None
            else:
                data[form_field] = input_value
        log.info(f"_validate_company_form | Collected company data: {data}")
        return data
    
    def _invalid_input_message(self, empty_input_field):
        self.popup.grab_release()
        self.popup.attributes("-disabled", True)
        messagebox.showwarning("Предупреждение", f"Моля, попълнете {empty_input_field}.")
        self.popup.attributes("-disabled", False)
        self.popup.grab_set()

    def _save_company(self, company=None):
        company_data = self._validate_company_form()
        if not company_data:
            return
        
        log.info(f"_save_company | Saving company data: {company_data}")

        # edit existing company
        if self.mode == 'edit':
            # Update existing company
            for field, value in company_data.items():
                setattr(company, field, value)
            edited_company = self.controller.update_company(company)
        elif self.mode == 'add':
            # Create new company
            new_company = Company(**company_data)
            new_company = self.controller.add_company(new_company)
        else:
            raise Exception("mode of company form is neither edit nor add")
        
        self._root.attributes("-disabled", False)
        self.popup.destroy()
        self.controller.destroy_company_form()
