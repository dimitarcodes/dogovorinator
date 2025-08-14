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

        entered = self.controller.get_entered_vars()

        review_text = "=== ПРЕГЛЕД НА ДАННИТЕ ===\n\n"
        
        review_text += "=== Данни на компанията ===\n"

        review_text += f"Име на фирмата (БГ): {entered.get('CMP_NAME_BG', 'Не е въведено')}\n"
        review_text += f"Име на фирмата (EN): {entered.get('CMP_NAME_EN', 'Не е въведено')}\n"
        review_text += f"Адрес (БГ): {entered.get('CMP_ADDR_BG', 'Не е въведено')}\n"
        review_text += f"Адрес (EN): {entered.get('CMP_ADDR_EN', 'Не е въведено')}\n"
        review_text += f"БУЛСТАТ: {entered.get('CMP_BULSTAT', 'Не е въведено')}\n"
        review_text += f"Представляващо лице (БГ): {entered.get('CMP_REPR_BG', 'Не е въведено')}\n"
        review_text += f"Представляващо лице (EN): {entered.get('CMP_REPR_EN', 'Не е въведено')}\n"

        review_text += "\n=== Данни на служителя ===\n"
        review_text += f"Име на служителя (БГ): {entered.get('MPL_NAME_BG', 'Не е въведено')}\n"
        review_text += f"Име на служителя (EN): {entered.get('MPL_NAME_EN', 'Не е въведено')}\n"
        review_text += f"Дата на раждане (БГ): {entered.get('MPL_DOB_BG', 'Не е въведено')}\n"
        review_text += f"Дата на раждане (EN): {entered.get('MPL_DOB_EN', 'Не е въведено')}\n"

        self.review_text.setPlainText(review_text)

    def _generate_contract(self):
        """Handle contract generation"""
        self.show_info("Генериране", "Договорът ще бъде генериран (функционалност в разработка).")
        log.info("Contract generation requested")
