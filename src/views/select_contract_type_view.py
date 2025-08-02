from src.views import AbstractView
from src.logger import DogovLogger

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, font

log = DogovLogger.get_logger()
class SelectContractTypeView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = ttk.Label(self.main_frame, text="Изберете тип договор:")
        
        # Companies frame
        self.contracts_type_frame = ttk.LabelFrame(self.main_frame, text="Типове договори", padding="10")

        # Navigation frame
        self.nav_frame = ttk.Frame(self.main_frame)
        # Navigation buttons
        self.back_button = ttk.Button(self.nav_frame, text="Назад", command=self.controller.prev_step)
        # self.start_button = ttk.Button(self.nav_frame, text="Начало") #, command=self.controller.start)


        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.title_label.pack(pady=(0, 20))

        self.contracts_type_frame.pack(fill=tk.BOTH, pady=(0, 20))

        buttons = {}
        for template in self.controller.get_available_templates():
            buttons[template] = ttk.Button(self.contracts_type_frame, text=template, command=lambda t=template: self._select_contract(t))
            buttons[template].pack(side=tk.TOP, pady=(10, 0))
        
        self.nav_frame.pack(fill="x", pady=(20, 0),side="bottom")
        self.back_button.pack(side="left",)
        # self.start_button.pack(side="left", padx=(10, 0))

    def _select_contract(self, contract_type):
        self.controller.set_selected_contract_template(contract_type)
        self.controller.next_step()