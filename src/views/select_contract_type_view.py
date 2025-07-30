
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font
from src.views.abstract_view import AbstractView

class SelectContractTypeView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Изберете тип договор:")
        
        # Companies frame
        self.contracts_type_frame = ttk.LabelFrame(self.main_frame, text="Типове договори", padding="10")

        self.contract_type1_button = ttk.Button(self.contracts_type_frame, text="Тип 1", padding="5", command=lambda: self._select_contract(1))
        self.contract_type2_button = ttk.Button(self.contracts_type_frame, text="Тип 2", padding="5", command=lambda: self._select_contract(2))
        self.contract_type3_button = ttk.Button(self.contracts_type_frame, text="Тип 3", padding="5", command=lambda: self._select_contract(3))

        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        self.back_button = ttk.Button(self.nav_frame, text="Назад" ) #, command=self.go_back)
        self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.go_to_start)


        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))

        self.contracts_type_frame.pack(fill=tk.BOTH, pady=(0, 20))

        self.contract_type1_button.pack(side=tk.TOP, pady=(10, 0))
        self.contract_type2_button.pack(side=tk.TOP, pady=(10, 0))
        self.contract_type3_button.pack(side=tk.TOP, pady=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")
        self.back_button.pack(side="left")
        self.start_button.pack(side="left", padx=(10, 0))

    def _select_contract(self, contract_type):
        self.controller.set_selected_contract_type(contract_type)
        self.controller.next_step()