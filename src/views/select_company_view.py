from src.models.entities import Company
from src.views import AbstractView
from src.logger import DogovLogger

import tkinter as tk
from tkinter import ttk, messagebox

log = DogovLogger.get_logger()

class SelectCompanyView(AbstractView):

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
        
        
        # Companies Treeview
        # Using Treeview for better column support
        self.companies_treeview = ttk.Treeview(self.companies_frame,
                                                columns=("id", "name", "vat_number"),
                                                show='headings',
                                                height=10)
        
        self.companies_treeview.heading("id", 
                                        text="#",
                                        command=lambda: self.sort_column(self.companies_treeview, "id", False))
        
        self.companies_treeview.heading("name", 
                                        text="Име на фирмата", 
                                        command=lambda: self.sort_column(self.companies_treeview, "name", False))
        
        self.companies_treeview.heading("vat_number", 
                                        text="БУЛСТАТ",
                                        command=lambda: self.sort_column(self.companies_treeview, "vat_number", False))
        
        self.companies_treeview.column("id", width=10, anchor="center")

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
        self.companies_treeview.pack(fill=tk.BOTH, pady=(0, 10))
        self.companies_treeview.bind("<Double-Button-1>", lambda _ : self._go_next())
        self.del_company_button.pack(side="left", padx=(10, 0))
        self.edit_company_button.pack(side="left", padx=(10, 0))
        self.add_company_button.pack(side="right", padx=(10, 0))

        self.next_button.pack(side="right", padx=(10, 0))        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")

        self.reload_treeview()
        self.companies_treeview.bind("<<TreeviewSelect>>", lambda e : log.info(f"selection output: {self.companies_treeview.selection()}"))


    def reload_treeview(self):
        # destroy all children
        for item in self.companies_treeview.get_children():
            self.companies_treeview.delete(item)

        # repopulate with companies
        for idx, company in enumerate(self.controller.get_companies()):
            # visible stuff
            vals = (str(idx + 1), company.name, company.vat_number)
            # iid links it back to the companies list
            item_id = self.companies_treeview.insert("", "end", values = vals, iid = idx)
            log.info(f"Company {company.name} added to listbox with id {item_id}")
        
    def sort_column(self, tree, col, reverse):
        """
        sort function for the treeview columns
        """
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        # Sort the data based on the column
        data.sort(reverse=reverse)
        # Rearrange the items in the sorted order
        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)
        # Reverse the sort order for the next click
        tree.heading(col, command=lambda: self.sort_column(tree, col, not reverse))

    def _select_company(self, task="да продължите"):
        selection = self.companies_treeview.selection()
        if not selection:
            messagebox.showwarning("Предупреждение", f"Моля, изберете фирма от списъка за {task}.")
            return
        log.info(f"selection: {selection}")
        sel_idx = int(selection[0])
        sel_company = self.controller.get_companies()[sel_idx]
        return sel_company

    def _go_next(self):
        selected_company = self._select_company(task="да продължите")
        if not selected_company:
            return
        self.controller.set_selected_company(selected_company)
        self.controller.next_step()

    def _del_company(self):
        selected_company = self._select_company(task="изтриване")
        if not selected_company:
            return
        self.controller.remove_company(selected_company)
        
    def _edit_company(self):
        selected_company = self._select_company(task="редактиране")
        if not selected_company:
            return
        self.controller.edit_company_dialog(selected_company)
    
    def _add_company(self):
        self.controller.add_company_dialog()
