
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
class SelectCompanyView:
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = ttk.Label(self.main_frame, 
                                        text="Изберете фирма или въведете нова",
                                        font=("century schoolbook l", 16, 'bold')
                                     )
        
        # Companies frame
        self.companies_frame = ttk.LabelFrame(self.main_frame, text="Съществуващи компании", padding="10")
        # Companies listbox
        self.companies_listbox = tk.Listbox(self.companies_frame, font=('Arial', 20), height=10)
        # Companies edit and delete buttons
        self.edit_company_button = ttk.Button(self.companies_frame, text="Редактиране", padding="5") 
        self.del_company_button = ttk.Button(self.companies_frame, text="Изтриване", padding="5") 
        # self.next_button = ttk.Button(self.companies_frame, text="Напред", command=self.go_next, padding="5") 
        

        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        # self.back_button = ttk.Button(self.nav_frame, text="Назад" ) #, command=self.go_back)
        # self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.go_to_start)
        self.next_button = ttk.Button(self.nav_frame, text="Напред", command=self.go_next, padding="5") 

        self.hide()

    def go_next(self):
        selected_index = self.companies_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Предупреждение", "Моля, изберете фирма от списъка.")
            return
        
        selected_company = self.companies[selected_index[0]]
        self.controller.set_selected_company(selected_company)
        self.controller.next_step()

    def load_companies(self):
        self.companies_listbox.delete(0, tk.END)
        self.companies = self.controller.get_companies()
        
        for company in self.companies:
            display_text = f"{company['name']} - {company['vat_number']}"
            self.companies_listbox.insert(tk.END, display_text)
            
    def set_controller(self, controller):
        self.controller = controller
        self.load_companies()
        # self.next_button.config(command = controller.next_step)

    def show(self):

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))

        self.companies_frame.pack(fill=tk.BOTH, pady=(0, 20))
        self.companies_listbox.pack(fill=tk.BOTH, pady=(0, 10))
        
        self.del_company_button.pack(side="left", padx=(10, 0))
        self.edit_company_button.pack(side="left", padx=(10, 0))
        self.next_button.pack(side="right", padx=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")
        # self.back_button.pack(side="left")
        # self.start_button.pack(side="left", padx=(10, 0))

    def hide(self):
        # pass
        self.main_frame.pack_forget()