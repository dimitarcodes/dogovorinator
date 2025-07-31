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
        self.companies_listbox = tk.Listbox(self.companies_frame, font=('Arial', 14), height=10)
        for company in self.companies:
            display_text = f"{company['name']} - {company['vat_number']}"
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
        
        self.del_company_button.pack(side="left", padx=(10, 0))
        self.edit_company_button.pack(side="left", padx=(10, 0))
        self.next_button.pack(side="right", padx=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")

    def _go_next(self):
        selected_index = self.companies_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Предупреждение", "Моля, изберете фирма от списъка.")
            return
        
        selected_company = self.companies[selected_index[0]]
        self.controller.set_selected_company(selected_company)
        self.controller.next_step()

    def _del_company(self):
        selected_index = self.companies_listbox.curselection()
        selected_company = self.companies[selected_index[0]]

        log.info(f"Deleting company - {selected_company}. To be implemented...")

    def _edit_company(self):
        selected_index = self.companies_listbox.curselection()
        selected_company = self.companies[selected_index[0]]
        log.info(f"Editing company - {selected_company}. To be implemented...")