from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                              QLineEdit, QFormLayout, QDateEdit, QComboBox,
                              QGroupBox, QFrame, QTextEdit, QSpinBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class ContractDetailsFormView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = QLabel("Въведете данни за договора:")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Form frame
        self.form_frame = QGroupBox("Детайли на договора")
        form_layout = QFormLayout()
        self.form_frame.setLayout(form_layout)
        
        # Employee details
        self.employee_name_edit = QLineEdit()
        self.employee_egn_edit = QLineEdit()
        self.position_edit = QLineEdit()
        self.salary_spinbox = QSpinBox()
        self.salary_spinbox.setRange(0, 999999)
        self.salary_spinbox.setSuffix(" лв.")
        
        self.start_date_edit = QDateEdit()
        self.start_date_edit.setDate(QDate.currentDate())
        self.start_date_edit.setCalendarPopup(True)
        
        # Add fields to form
        form_layout.addRow("Име на служител:", self.employee_name_edit)
        form_layout.addRow("ЕГН:", self.employee_egn_edit)
        form_layout.addRow("Длъжност:", self.position_edit)
        form_layout.addRow("Заплата:", self.salary_spinbox)
        form_layout.addRow("Дата на започване:", self.start_date_edit)
        
        # Navigation frame
        nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.controller.previous_step)
        
        self.start_button = QPushButton("Начало")
        self.start_button.clicked.connect(self.controller.go_to_start)
        
        self.next_button = QPushButton("Напред")
        self.next_button.clicked.connect(self._go_next)
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.start_button)
        nav_layout.addStretch()
        nav_layout.addWidget(self.next_button)
        
        nav_frame = QFrame()
        nav_frame.setLayout(nav_layout)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.form_frame)
        self.main_layout.addWidget(nav_frame)

    def _go_next(self):
        """Validate form and proceed to next step"""
        # Basic validation
        if not self.employee_name_edit.text().strip():
            self.show_warning("Грешка", "Моля, въведете име на служителя.")
            return
            
        if not self.employee_egn_edit.text().strip():
            self.show_warning("Грешка", "Моля, въведете ЕГН.")
            return
            
        if not self.position_edit.text().strip():
            self.show_warning("Грешка", "Моля, въведете длъжност.")
            return
        
        # Store form data (you might want to pass this to controller)
        self.employee_data = {
            'name': self.employee_name_edit.text().strip(),
            'egn': self.employee_egn_edit.text().strip(),
            'position': self.position_edit.text().strip(),
            'salary': self.salary_spinbox.value(),
            'start_date': self.start_date_edit.date().toPython()
        }

        self.controller.set_employee_data(self.employee_data)
        
        log.info(f"Employee data collected: {self.employee_data}")
        self.controller.next_step()
