from src.models.company_model import Company
from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, 
                              QTableWidgetItem, QPushButton, QHeaderView, 
                              QMessageBox, QGroupBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class SelectCompanyView(AbstractView):

    def _build_gui(self):
        # Main layout is already set in AbstractQtView
        
        # View Title - Instructions
        self.title_label = QLabel("Изберете фирма или въведете нова")
        title_font = QFont("Century Schoolbook L", 18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Companies frame (GroupBox in Qt)
        self.companies_frame = QGroupBox("Съществуващи компании")
        companies_layout = QVBoxLayout()
        self.companies_frame.setLayout(companies_layout)
        
        # Companies Table (QTableWidget instead of Treeview)
        self.companies_table = QTableWidget()
        self.companies_table.setColumnCount(2)
        self.companies_table.setHorizontalHeaderLabels(["БУЛСТАТ", "Име на фирмата"])
        
        # Configure table columns
        header = self.companies_table.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # ID column
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents )  # BULSTAT column resize to contents + a bit of padding
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Name column stretches to fill space

        # Set selection behavior
        self.companies_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.companies_table.setSelectionMode(QTableWidget.SingleSelection)
        
        # Double-click to proceed
        self.companies_table.itemDoubleClicked.connect(self._go_next)
        
        # Button layout for company operations
        company_buttons_layout = QHBoxLayout()
        
        self.del_company_button = QPushButton("Изтриване")
        self.del_company_button.clicked.connect(self._del_company)
        
        self.edit_company_button = QPushButton("Редактиране") 
        self.edit_company_button.clicked.connect(self._edit_company)
        
        self.add_company_button = QPushButton("Добавяне на нова фирма")
        self.add_company_button.clicked.connect(self._add_company)
        
        # Add buttons to layout
        company_buttons_layout.addWidget(self.del_company_button)
        company_buttons_layout.addWidget(self.edit_company_button)
        company_buttons_layout.addStretch()  # Push next button to the right
        company_buttons_layout.addWidget(self.add_company_button)
        
        # Add table and buttons to companies frame
        companies_layout.addWidget(self.companies_table)
        companies_layout.addLayout(company_buttons_layout)
        
        # Navigation frame
        nav_layout = QHBoxLayout()
        nav_layout.addStretch()  # Push button to the right
        
        self.next_button = QPushButton("Напред")
        self.next_button.clicked.connect(self._go_next)
        nav_layout.addWidget(self.next_button)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.companies_frame)
        
        # Add some spacing before navigation
        nav_frame = QFrame()
        nav_frame.setLayout(nav_layout)
        self.main_layout.addWidget(nav_frame)
        
        # Load companies data
        self.reload_table()

    def reload_table(self):
        """Reload the companies table with current data"""
        self.companies_table.setRowCount(0)  # Clear existing rows
        
        companies = self.controller.get_companies()
        self.companies_table.setRowCount(len(companies))
        
        for idx, company in enumerate(companies):
            # Add row data
            # id_item = QTableWidgetItem(str(idx))
            
            bulstat_item = QTableWidgetItem(company.bulstat)
            name_item = QTableWidgetItem(company.name_bg)
            
            # Set items in table
            self.companies_table.setItem(idx, 0, bulstat_item)
            self.companies_table.setItem(idx, 1, name_item)

            log.info(f"Company {company.name_bg} added to table with row {idx}")
    
    def reload_treeview(self):
        """Compatibility method name - calls reload_table"""
        self.reload_table()

    def _select_company(self, task="да продължите"):
        """Get the currently selected company"""
        current_row = self.companies_table.currentRow()
        if current_row == -1:
            self.show_warning("Предупреждение", f"Моля, изберете фирма от списъка за {task}.")
            return None
        
        companies = self.controller.get_companies()
        if current_row < len(companies):
            return companies[current_row]
        return None

    def _go_next(self):
        """Handle next button click or double-click on table"""
        selected_company = self._select_company(task="да продължите")
        if not selected_company:
            return
        self.controller.set_selected_company(selected_company)
        self.controller.next_step()

    def _del_company(self):
        """Handle delete company button click"""
        selected_company = self._select_company(task="изтриване")
        if not selected_company:
            return
        
        # Confirm deletion
        if self.ask_yes_no("Потвърждение", f"Сигурни ли сте, че искате да изтриете {selected_company.name_bg}?"):
            self.controller.remove_company(selected_company)
        
    def _edit_company(self):
        """Handle edit company button click"""
        selected_company = self._select_company(task="редактиране")
        if not selected_company:
            return
        self.controller.edit_company_dialog(selected_company)
    
    def _add_company(self):
        """Handle add company button click"""
        self.controller.add_company_dialog()
