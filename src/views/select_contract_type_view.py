from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                              QGroupBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class SelectContractTypeView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = QLabel("Изберете тип договор:")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Contract types frame
        self.contracts_type_frame = QGroupBox("Типове договори")
        contracts_layout = QVBoxLayout()
        self.contracts_type_frame.setLayout(contracts_layout)
        
        # Contract type buttons
        self.contract_type1_button = QPushButton("Постоянен трудов договор")
        self.contract_type1_button.clicked.connect(lambda: self._select_contract("template"))
        
        self.contract_type2_button = QPushButton("Срочен трудов договор")
        self.contract_type2_button.clicked.connect(lambda: self._select_contract("template"))
        
        # Add buttons to layout with some spacing
        contracts_layout.addWidget(self.contract_type1_button)
        contracts_layout.addWidget(self.contract_type2_button)
        contracts_layout.addStretch()  # Add stretch to push buttons to top
        
        # Navigation frame
        nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.controller.previous_step)
        
        self.start_button = QPushButton("Начало")
        self.start_button.clicked.connect(self.controller.go_to_start)
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.start_button)
        nav_layout.addStretch()  # Push buttons to the left
        
        nav_frame = QFrame()
        nav_frame.setLayout(nav_layout)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.contracts_type_frame)
        self.main_layout.addWidget(nav_frame)

    def _select_contract(self, contract_type):
        """Handle contract type selection"""
        log.info(f"Selected contract type: {contract_type}")
        self.controller.set_selected_contract_type(contract_type)
        self.controller.next_step()
