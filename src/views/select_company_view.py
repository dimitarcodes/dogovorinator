from src.models.entities import Company
from src.views import AbstractView
from src.logger import DogovLogger

import tkinter as tk
from tkinter import ttk, messagebox

log = DogovLogger.get_logger()

class SelectCompanyView(AbstractView):

    def _init_logic(self):
        # get previously entered companies from the database
        self.companies = self.controller.get_companies()
          

    def _build_gui(self):
        # View Title - Instructions
        self.title_label = ttk.Label(self.main_frame, 
                                        text="Изберете фирма или въведете нова",
                                        font=("century schoolbook l", 18, 'bold')
                                    )
        
        s = ttk.Style()
        s.configure('Red.TLabelframe.Label', font=('courier', 15, 'bold'))
        # Companies frame
        self.companies_frame = ttk.LabelFrame(self.main_frame, 
                                                text="Съществуващи компании",
                                                padding="10",
                                                style="Red.TLabelframe")
        
        # Companies listbox
        self.companies_listbox = tk.Listbox(self.companies_frame,
                                            font=('Arial', 14),
                                            height=10,
                                            selectmode=tk.SINGLE,
                                            highlightthickness=2)
        for company in self.companies:
            display_text = f"{company.name} - {company.vat_number}"
            self.companies_listbox.insert(tk.END, display_text)

        # Companies edit and delete buttons
        self.edit_company_button = ttk.Button(self.companies_frame,
                                                text="Редактиране",
                                                padding="5",
                                                command=self._edit_company)

        self.del_company_button = ttk.Button(self.companies_frame,
                                                text="Изтриване", 
                                                padding="5",
                                                command=self._del_company) 
        self.add_company_button = ttk.Button(self.companies_frame,
                                                text="Добавяне на нова фирма",
                                                padding="5",
                                                command=self._add_company)
        
        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        self.next_button = ttk.Button(self.nav_frame,
                                        text="Напред",
                                        command=self._go_next,
                                        padding="5") 


        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))

        self.companies_frame.pack(fill=tk.BOTH, pady=(0, 20))
        self.companies_listbox.pack(fill=tk.BOTH, pady=(0, 10))
        self.companies_listbox.bind("<Double-Button-1>", lambda _ : self._go_next())
        self.del_company_button.pack(side="left", padx=(10, 0))
        self.edit_company_button.pack(side="left", padx=(10, 0))
        self.add_company_button.pack(side="right", padx=(10, 0))

        self.next_button.pack(side="right", padx=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")

    def _go_next(self):
        selected_index_obj = self.companies_listbox.curselection()
        if not selected_index_obj:
            messagebox.showwarning("Предупреждение", "Моля, изберете фирма от списъка за да продължите.")
            return
        self.selected_index = selected_index_obj[0]

        log.info(f"selected_index: {self.selected_index} for selection")

        selected_company = self.companies[self.selected_index]
        self.controller.set_selected_company(selected_company)
        self.controller.next_step()

    def _del_company(self):
        selected_index_obj = self.companies_listbox.curselection()
        if not selected_index_obj:
            messagebox.showwarning("Предупреждение", "Моля, изберете фирма от списъка за изтриване.")
            return
        self.selected_index = selected_index_obj[0]
        log.info(f"selected_index: {self.selected_index} for deletion")
        selected_company = self.companies[self.selected_index]

        if self.controller.remove_company(selected_company):
            self.companies_listbox.delete(self.selected_index)
        self.companies.pop(self.selected_index)
        log.info(f"Company removed: {selected_company}")
        
        # log.info(f"Deleting company - {selected_company}. To be implemented...")

    def _edit_company(self):
        selected_index_obj = self.companies_listbox.curselection()
        if not selected_index_obj:
            messagebox.showwarning("Предупреждение", "Моля, изберете фирма от списъка за редактиране.")
            return
        self.selected_index = selected_index_obj[0]
        selected_company = self.companies[self.selected_index]
        log.info(f"selected_index: {self.selected_index} for editing")
        self._company_popup(selected_company)
        log.info(f"Editing company - {selected_company}. To be implemented...")

    def _add_company(self):
        self._company_popup()
    
    def _company_popup(self, company=None):
        if company is None:
            company_form_win_name = "Добавяне на нова фирма"
        else:
            company_form_win_name = "Редактиране на фирма"
        self.company_form_win = tk.Toplevel(self._root)
        self.company_form_win.transient(self._root)
        self.company_form_win.wm_title(company_form_win_name)
        self.company_form_win.geometry("400x300")
        self.company_form_win.grab_set()
        self._root.attributes("-disabled", True)

        self._position_company_form_win()
        self.company_form_win.protocol("WM_DELETE_WINDOW", lambda: self._on_company_form_close())

        company_frame = ttk.LabelFrame(self.company_form_win, text="Детайли на компанията", padding=20)
        company_frame.pack(fill=tk.BOTH, pady=(0, 10))

        self.company_form = {}
        for field in Company.get_fields():
            
            # set the widget's name for easy access later
            label = ttk.Label(company_frame, text=field)
            entry = ttk.Entry(company_frame)
            self.company_form[field] = entry

            label.pack()
            entry.pack()

            if company and hasattr(company, field):
                entry.insert(0, getattr(company, field))
        
        nav_frame = ttk.Frame(self.company_form_win)
        nav_frame.pack(fill=tk.X, pady=(10, 0))
        save_button = ttk.Button(nav_frame, text="Запази", command=lambda: self._save_company(company))
        save_button.pack(side=tk.RIGHT, padx=(0, 10))

    def _position_company_form_win(self):
        # Center the popup window on the main window
        x = self._root.winfo_x() + (self._root.winfo_width() // 2) - 200
        y = self._root.winfo_y() + (self._root.winfo_height() // 2) - 150
        self.company_form_win.geometry(f"+{x}+{y}")
    def _on_company_form_close(self):
        self._root.attributes("-disabled", False)
        self.company_form_win.destroy()
        log.info("Company form closed without saving.")

    def _collect_validate_company_form(self):
        data = {}
        for form_field in self.company_form:
            input_value = self.company_form[form_field].get().strip()
            if not input_value:
                self.company_form_win.grab_release()
                
                self.company_form_win.attributes("-disabled", True)
                messagebox.showwarning("Предупреждение", f"Моля, попълнете {form_field}.")
                
                self.company_form_win.attributes("-disabled", False)
                self.company_form_win.grab_set()
                return None
            else:
                data[form_field] = input_value
        log.info(f"Collected company data: {data}")
        return data
    
    def _save_company(self, company=None):
        validated_company_data = self._collect_validate_company_form()
        if not validated_company_data:
            return
        fields = Company.get_fields()
    
        log.info(f"Saving company data: {validated_company_data}")

        display_text = f"{validated_company_data['name']} - {validated_company_data['vat_number']}"
        # edit existing company
        if company:
            # Update existing company
            for field, value in validated_company_data.items():
                setattr(company, field, value)
            new_company = self.controller.update_company(company)
            self.companies[self.selected_index] = new_company
            self.companies_listbox.delete(self.selected_index)
            self.companies_listbox.insert(self.selected_index, display_text)
        # add new company
        else:
            # Create new company
            new_company = Company(**validated_company_data)
            new_company = self.controller.add_company(new_company)
            self.companies.append(new_company)
            self.companies_listbox.insert(tk.END, display_text)
        # update the listbox UI

        self._root.attributes("-disabled", False)
        self.company_form_win.destroy()

