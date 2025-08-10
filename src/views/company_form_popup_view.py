from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                                QPushButton, QLineEdit, QFormLayout, QGroupBox,
                                QMessageBox, QDialogButtonBox)
from PySide6.QtCore import Qt
from src.models.entities import Company
from src.logger import DogovLogger

log = DogovLogger.get_logger()

class CompanyFormPopupView(QDialog):
    def __init__(self, parent, controller, company: Company = None):
        super().__init__(parent)
        self.controller = controller
        self.company = company
        self.mode = "edit" if company else "add"
        
        self.setModal(True)  # Make it modal
        self.setFixedSize(400, 300)
        self._build_gui()
        self._center_on_parent()

    def _build_gui(self):
        popup_title = "Редактиране на фирма" if self.mode == "edit" else "Добавяне на фирма"
        self.setWindowTitle(popup_title)
        
        # Main layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)
        
        # Company form group
        self.company_frame = QGroupBox("Детайли на компанията")
        form_layout = QFormLayout()
        self.company_frame.setLayout(form_layout)
        
        # Create form fields
        self.company_form = {}
        for field in Company.get_fields():
            entry = QLineEdit()
            self.company_form[field] = entry
            
            # Set existing values if editing
            if self.company and hasattr(self.company, field):
                entry.setText(str(getattr(self.company, field)))
            
            form_layout.addRow(f"{field}:", entry)
        
        # Button box for Save/Cancel
        button_box = QDialogButtonBox()
        save_button = button_box.addButton("Запази", QDialogButtonBox.AcceptRole)
        cancel_button = button_box.addButton("Отказ", QDialogButtonBox.RejectRole)
        
        save_button.clicked.connect(self._save_company)
        cancel_button.clicked.connect(self.reject)
        
        # Add to main layout
        main_layout.addWidget(self.company_frame)
        main_layout.addWidget(button_box)

    def _center_on_parent(self):
        """Center the dialog on the parent window"""
        if self.parent():
            parent_geometry = self.parent().geometry()
            x = parent_geometry.x() + (parent_geometry.width() - self.width()) // 2
            y = parent_geometry.y() + (parent_geometry.height() - self.height()) // 2
            self.move(x, y)

    def _validate_company_form(self):
        """Validate form data and return company data dict"""
        data = {}
        for form_field, entry in self.company_form.items():
            input_value = entry.text().strip()
            if not input_value:
                QMessageBox.warning(self, "Грешка", f"Полето '{form_field}' е задължително.")
                return None
            data[form_field] = input_value
        return data

    def _save_company(self):
        """Save the company data"""
        data = self._validate_company_form()
        if not data:
            return
        
        try:
            if self.mode == "add":
                # Create new company
                new_company = Company(**data)
                self.controller.add_company(new_company)
                log.info(f"Company added: {new_company}")
            else:
                # Update existing company
                for field, value in data.items():
                    setattr(self.company, field, value)
                self.controller.update_company(self.company)
                log.info(f"Company updated: {self.company}")
            
            self.accept()  # Close dialog with success
            
        except Exception as e:
            log.error(f"Error saving company: {e}")
            QMessageBox.critical(self, "Грешка", f"Грешка при запазването: {str(e)}")

    def reject(self):
        """Handle dialog cancellation"""
        log.info("Company form cancelled.")
        self.controller.destroy_company_form()
        super().reject()

    def accept(self):
        """Handle dialog acceptance"""
        self.controller.destroy_company_form()
        super().accept()
