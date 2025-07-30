
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font

class SelectContractTypeView:
    def __init__(self, root: tk.Tk):
        self.root = root
        
        # Main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Изберете тип договор:")
        
        # Companies frame
        self.contracts_type_frame = ttk.LabelFrame(self.main_frame, text="Типове договори", padding="10")

        self.contract_type1_button = ttk.Button(self.contracts_type_frame, text="Тип 1", padding="5", command=self.go_next_one)
        self.contract_type2_button = ttk.Button(self.contracts_type_frame, text="Тип 2", padding="5", command=self.go_next_two)
        self.contract_type3_button = ttk.Button(self.contracts_type_frame, text="Тип 3", padding="5", command=self.go_next_three)

        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        self.back_button = ttk.Button(self.nav_frame, text="Назад" ) #, command=self.go_back)
        self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.go_to_start)
        self.next_button = ttk.Button(self.nav_frame, text="Напред", command=self.go_next, padding="5") 

        self.hide()

    def go_next_one(self):
        self.go_next(type_contract="type1")
    def go_next_two(self):
        self.go_next(type_contract="type2")
    def go_next_three(self):
        self.go_next(type_contract="type3")

    def go_next(self, type_contract=None):
        self.controller.set_selected_contract_type(type_contract)
        self.controller.next_step()

    def set_controller(self, controller):
        self.controller = controller
        # self.next_button.config(command = controller.next_step)

    def show(self):

        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))

        self.contracts_type_frame.pack(fill=tk.BOTH, pady=(0, 20))

        self.contract_type1_button.pack(side=tk.TOP, pady=(10, 0))
        self.contract_type2_button.pack(side=tk.TOP, pady=(10, 0))
        self.contract_type3_button.pack(side=tk.TOP, pady=(10, 0))

        self.next_button.pack(side="right", padx=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")
        self.back_button.pack(side="left")
        self.start_button.pack(side="left", padx=(10, 0))

    def hide(self):
        self.main_frame.pack_forget()