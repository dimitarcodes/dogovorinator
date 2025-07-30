
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class SelectCompanyViewBak:
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure root grid
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Изберете фирма или въведете нова", 
                                    font=('Arial', 16, 'bold'))
        self.title_label.grid(row=0, column=0, pady=(0, 20))
        
        # Content frame (changes for each step)
        self.content_frame = ttk.Frame(self.main_frame)
        self.content_frame.grid(row=1, column=0, sticky="nsew")

        # Existing companies frame
        self.companies_frame = ttk.LabelFrame(self.content_frame, text="Съществуващи компании", padding="10")
        self.companies_frame.pack(fill="x", pady=(0, 20))

        # Companies listbox
        self.companies_listbox = tk.Listbox(self.companies_frame, height=6)


        # Load companies
        # self.load_companies()
        
        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        self.nav_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        # Navigation buttons
        self.back_button = ttk.Button(self.nav_frame, text="Назад" ) #, command=self.go_back)
        self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.go_to_start)
        self.edit_company_button = ttk.Button(self.companies_frame, text="Редактиране") 
        self.del_company_button = ttk.Button(self.companies_frame, text="Изтриване") 
        self.next_button = ttk.Button(self.companies_frame, text="Напред", command=self.go_next) #, command=self.go_next)
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
        self.companies_listbox.pack(fill="x", pady=(0, 10))
        self.back_button.pack(side="left")
        self.start_button.pack(side="left", padx=(10, 0))
        self.del_company_button.pack(side="left", padx=(10, 0))
        self.next_button.pack(side="right")
        self.edit_company_button.pack(side="left")
        

    def hide(self):
        # pass
        self.main_frame.pack_forget()