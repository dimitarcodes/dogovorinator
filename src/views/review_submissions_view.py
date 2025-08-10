from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                              QTextEdit, QGroupBox, QFrame)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class ReviewSubmissionsView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = QLabel("Преглед и генериране на договор:")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Review frame
        self.review_frame = QGroupBox("Преглед на данните")
        review_layout = QVBoxLayout()
        self.review_frame.setLayout(review_layout)
        
        # Review text area
        self.review_text = QTextEdit()
        self.review_text.setReadOnly(True)
        review_layout.addWidget(self.review_text)
        
        # Generate button
        self.generate_button = QPushButton("Генериране на договор")
        self.generate_button.clicked.connect(self._generate_contract)
        review_layout.addWidget(self.generate_button)
        
        # Navigation frame
        nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.controller.previous_step)
        
        self.start_button = QPushButton("Начало")
        self.start_button.clicked.connect(self.controller.go_to_start)
        
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.start_button)
        nav_layout.addStretch()
        
        nav_frame = QFrame()
        nav_frame.setLayout(nav_layout)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.review_frame)
        self.main_layout.addWidget(nav_frame)

    def show(self):
        """Override show to update review text when view becomes visible"""
        super().show()
        self._update_review_text()

    def _update_review_text(self):
        """Update the review text with current selections"""
        log.info("Updating review text")
        company = self.controller.get_selected_company()
        contract_type = self.controller.get_selected_contract_type()
        employee_data = self.controller.get_employee_data()

        review_text = "=== ПРЕГЛЕД НА ДАННИТЕ ===\n\n"
        
        if company:
            for field, label in company.get_fields_with_labels().items():
                review_text += f"{label}: {getattr(company, field, 'N/A')}\n"

        if contract_type:
            contract_type_name = "Постоянен трудов договор" if contract_type == "permanent" else "Срочен трудов договор"
            review_text += f"Тип договор: {contract_type_name}\n\n"

        if employee_data:
            for k, v in employee_data.items():
                review_text += f"{k}: {v}\n"

        self.review_text.setPlainText(review_text)

    def _generate_contract(self):
        """Handle contract generation"""
        self.show_info("Генериране", "Договорът ще бъде генериран (функционалност в разработка).")
        log.info("Contract generation requested")
