from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                              QLineEdit, QFormLayout, QDateEdit, QComboBox,
                              QGroupBox, QFrame, QTextEdit, QSpinBox, 
                              QScrollArea, QWidget, QCheckBox, QDoubleSpinBox)
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class ContractDetailsFormScrollableView(AbstractView):

    def _build_gui(self):
        # Title
        self.title_label = QLabel("Въведете данни за договора:")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setAlignment(Qt.AlignCenter)
        
        # Create scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Create scrollable widget
        self.scroll_widget = QWidget()
        self.scroll_layout = QVBoxLayout()
        self.scroll_widget.setLayout(self.scroll_layout)
        
        # Employee Personal Information Section
        self.personal_info_frame = QGroupBox("Лични данни на служителя")
        self.personal_layout = QFormLayout()
        self.personal_info_frame.setLayout(self.personal_layout)
        
        
        
        # # Position and Work Details Section
        # self.work_details_frame = QGroupBox("Данни за работното място")
        # work_layout = QFormLayout()
        # self.work_details_frame.setLayout(work_layout)
        
        # self.position_edit = QLineEdit()
        # self.position_edit.setPlaceholderText("Длъжност според КИД")
        # self.department_edit = QLineEdit()
        # self.department_edit.setPlaceholderText("Отдел/Департament")
        # self.work_location_edit = QLineEdit()
        # self.work_location_edit.setPlaceholderText("Адрес на работното място")
        # self.immediate_supervisor_edit = QLineEdit()
        # self.immediate_supervisor_edit.setPlaceholderText("Име на директен ръководител")
        # self.work_schedule_combo = QComboBox()
        # self.work_schedule_combo.addItems(["8 часов работен ден", "Гъвкаво работно време", "Сменна работа", "Непълно работно време"])
        # self.probation_period_spinbox = QSpinBox()
        # self.probation_period_spinbox.setRange(0, 6)
        # self.probation_period_spinbox.setSuffix(" месеца")
        
        # work_layout.addRow("Длъжност:", self.position_edit)
        # work_layout.addRow("Отдел:", self.department_edit)
        # work_layout.addRow("Работно място:", self.work_location_edit)
        # work_layout.addRow("Непосредствен ръководител:", self.immediate_supervisor_edit)
        # work_layout.addRow("Работно време:", self.work_schedule_combo)
        # work_layout.addRow("Изпитателен срок:", self.probation_period_spinbox)
        
        # # Contract Terms Section
        # self.contract_terms_frame = QGroupBox("Условия на договора")
        # contract_layout = QFormLayout()
        # self.contract_terms_frame.setLayout(contract_layout)
        
        # self.start_date_edit = QDateEdit()
        # self.start_date_edit.setDate(QDate.currentDate())
        # self.start_date_edit.setCalendarPopup(True)
        # self.contract_type_combo = QComboBox()
        # self.contract_type_combo.addItems(["Безсрочен", "Срочен", "Временен", "Сезонен"])
        # self.contract_duration_spinbox = QSpinBox()
        # self.contract_duration_spinbox.setRange(0, 60)
        # self.contract_duration_spinbox.setSuffix(" месеца")
        # self.notice_period_spinbox = QSpinBox()
        # self.notice_period_spinbox.setRange(1, 3)
        # self.notice_period_spinbox.setSuffix(" месеца")
        # self.notice_period_spinbox.setValue(1)
        
        # contract_layout.addRow("Дата на започване:", self.start_date_edit)
        # contract_layout.addRow("Вид договор:", self.contract_type_combo)
        # contract_layout.addRow("Срок на договора:", self.contract_duration_spinbox)
        # contract_layout.addRow("Срок за предизвестие:", self.notice_period_spinbox)
        
        # # Salary and Benefits Section
        # self.salary_frame = QGroupBox("Възнаграждение и облаги")
        # salary_layout = QFormLayout()
        # self.salary_frame.setLayout(salary_layout)
        
        # self.salary_spinbox = QSpinBox()
        # self.salary_spinbox.setRange(0, 999999)
        # self.salary_spinbox.setSuffix(" лв.")
        # self.salary_spinbox.setValue(760)  # Minimum wage default
        # self.bonus_percentage_spinbox = QDoubleSpinBox()
        # self.bonus_percentage_spinbox.setRange(0, 100)
        # self.bonus_percentage_spinbox.setSuffix("%")
        # self.overtime_rate_spinbox = QDoubleSpinBox()
        # self.overtime_rate_spinbox.setRange(1.0, 3.0)
        # self.overtime_rate_spinbox.setValue(1.5)
        # self.overtime_rate_spinbox.setSingleStep(0.1)
        # self.paid_vacation_days_spinbox = QSpinBox()
        # self.paid_vacation_days_spinbox.setRange(20, 40)
        # self.paid_vacation_days_spinbox.setSuffix(" дни")
        # self.paid_vacation_days_spinbox.setValue(20)
        
        # self.health_insurance_checkbox = QCheckBox("Допълнително здравно осигуряване")
        # self.meal_vouchers_checkbox = QCheckBox("Ваучери за храна")
        # self.transport_allowance_checkbox = QCheckBox("Транспортни разходи")
        
        # salary_layout.addRow("Основна заплата:", self.salary_spinbox)
        # salary_layout.addRow("Бонус (%):", self.bonus_percentage_spinbox)
        # salary_layout.addRow("Ставка за извънредни часове:", self.overtime_rate_spinbox)
        # salary_layout.addRow("Платен годишен отпуск:", self.paid_vacation_days_spinbox)
        # salary_layout.addRow("", self.health_insurance_checkbox)
        # salary_layout.addRow("", self.meal_vouchers_checkbox)
        # salary_layout.addRow("", self.transport_allowance_checkbox)
        
        # # Additional Information Section
        # self.additional_info_frame = QGroupBox("Допълнителна информация")
        # additional_layout = QFormLayout()
        # self.additional_info_frame.setLayout(additional_layout)
        
        # self.education_level_combo = QComboBox()
        # self.education_level_combo.addItems(["Основно", "Средно", "Професионално", "Полувисше", "Висше", "Магистър", "Доктор"])
        # self.languages_edit = QLineEdit()
        # self.languages_edit.setPlaceholderText("Български, английски...")
        # self.special_requirements_edit = QTextEdit()
        # self.special_requirements_edit.setMaximumHeight(60)
        # self.special_requirements_edit.setPlaceholderText("Специални изисквания за работа")
        # self.confidentiality_checkbox = QCheckBox("Споразумение за поверителност")
        # self.non_compete_checkbox = QCheckBox("Клауза за неконкуренция")
        
        # additional_layout.addRow("Образование:", self.education_level_combo)
        # additional_layout.addRow("Езици:", self.languages_edit)
        # additional_layout.addRow("Специални изисквания:", self.special_requirements_edit)
        # additional_layout.addRow("", self.confidentiality_checkbox)
        # additional_layout.addRow("", self.non_compete_checkbox)
        
        # # Add all sections to scroll layout
        self.scroll_layout.addWidget(self.personal_info_frame)
        # scroll_layout.addWidget(self.work_details_frame)
        # scroll_layout.addWidget(self.contract_terms_frame)
        # scroll_layout.addWidget(self.salary_frame)
        # scroll_layout.addWidget(self.additional_info_frame)
        
        # Set scroll widget
        self.scroll_area.setWidget(self.scroll_widget)
        
        # Navigation frame
        self.nav_layout = QHBoxLayout()
        
        self.back_button = QPushButton("Назад")
        self.back_button.clicked.connect(self.controller.previous_step)
        
        self.start_button = QPushButton("Начало")
        self.start_button.clicked.connect(self.controller.go_to_start)
        
        self.next_button = QPushButton("Напред")
        self.next_button.clicked.connect(self._go_next)
        
        self.nav_layout.addWidget(self.back_button)
        self.nav_layout.addWidget(self.start_button)
        self.nav_layout.addStretch()
        self.nav_layout.addWidget(self.next_button)
        
        self.nav_frame = QFrame()
        self.nav_frame.setLayout(self.nav_layout)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(self.title_label)
        self.main_layout.addWidget(self.scroll_area)  # Add the scroll area instead of individual frames
        self.main_layout.addWidget(self.nav_frame)

    def get_concern(self, pretty_vars, concern):
        concern_vars = {}
        for var, props in pretty_vars.items():
            if props['concern'] == concern:
                concern_vars[var] = props
        return concern_vars
    
    def populate_forms(self):
        self.form_widgets = {}
        formvars = self.controller.get_formvars()
        empl_vars = self.get_concern(formvars, 'employee')

        for var, props in empl_vars.items():
            if props['type'] == 'date':
                entry = QDateEdit()
                entry.setDate(QDate.currentDate())
                entry.setCalendarPopup(True)
                self.personal_layout.addRow(props['hr_label'] + ":", entry)
                self.form_widgets[var] = entry
            else:
                entry = QLineEdit()
                # entry.setPlaceholderText(props['example'])
                self.form_widgets[var] = entry
                self.personal_layout.addRow(props['hr_label'] + ":", entry)

        # self.employee_name_edit = QLineEdit()
        # self.employee_name_edit.setPlaceholderText("Име, презиме, фамилия")
        # self.employee_egn_edit = QLineEdit()
        # self.employee_egn_edit.setPlaceholderText("XXXXXXXXXX")
        # self.employee_id_card_edit = QLineEdit()
        # self.employee_id_card_edit.setPlaceholderText("Номер на лична карта")
        # self.employee_phone_edit = QLineEdit()
        # self.employee_phone_edit.setPlaceholderText("+359XXXXXXXXX")
        # self.employee_email_edit = QLineEdit()
        # self.employee_email_edit.setPlaceholderText("email@example.com")
        # self.employee_address_edit = QTextEdit()
        # self.employee_address_edit.setMaximumHeight(60)
        # self.employee_address_edit.setPlaceholderText("Пълен адрес")
        # self.birth_date_edit = QDateEdit()
        # self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))
        # self.birth_date_edit.setCalendarPopup(True)
        # self.birth_place_edit = QLineEdit()
        # self.birth_place_edit.setPlaceholderText("Град, страна")
        
        # self.personal_layout.addRow("Име на служител:", self.employee_name_edit)
        # self.personal_layout.addRow("ЕГН:", self.employee_egn_edit)
        # self.personal_layout.addRow("Лична карта №:", self.employee_id_card_edit)
        # self.personal_layout.addRow("Телефон:", self.employee_phone_edit)
        # self.personal_layout.addRow("Email:", self.employee_email_edit)
        # self.personal_layout.addRow("Адрес:", self.employee_address_edit)
        # self.personal_layout.addRow("Дата на раждане:", self.birth_date_edit)
        # self.personal_layout.addRow("Място на раждане:", self.birth_place_edit)

    def _go_next(self):
        """Validate form and proceed to next step"""
        # Basic validation for required fields
        # required_fields = [
            # (self.employee_name_edit, "име на служителя"),
            # (self.employee_egn_edit, "ЕГН"),
            # (self.position_edit, "длъжност"),
        # ]
        
        # for field, field_name in required_fields:
        #     if not field.text().strip():
        #         self.show_warning("Грешка", f"Моля, въведете {field_name}.")
        #         field.setFocus()
        #         return
        
        # Collect all form data
        self.employee_data = {}
        for var, entry in self.form_widgets.items():
            if isinstance(entry, QDateEdit):
                self.employee_data[var] = entry.date().toPython()
            else:
                self.employee_data[var] = entry.text().strip()
            
        #     # Work Details
        #     'position': self.position_edit.text().strip(),
        #     'department': self.department_edit.text().strip(),
        #     'work_location': self.work_location_edit.text().strip(),
        #     'supervisor': self.immediate_supervisor_edit.text().strip(),
        #     'work_schedule': self.work_schedule_combo.currentText(),
        #     'probation_period': self.probation_period_spinbox.value(),
            
        #     # Contract Terms
        #     'start_date': self.start_date_edit.date().toPython(),
        #     'contract_type': self.contract_type_combo.currentText(),
        #     'contract_duration': self.contract_duration_spinbox.value(),
        #     'notice_period': self.notice_period_spinbox.value(),
            
        #     # Salary and Benefits
        #     'salary': self.salary_spinbox.value(),
        #     'bonus_percentage': self.bonus_percentage_spinbox.value(),
        #     'overtime_rate': self.overtime_rate_spinbox.value(),
        #     'vacation_days': self.paid_vacation_days_spinbox.value(),
        #     'health_insurance': self.health_insurance_checkbox.isChecked(),
        #     'meal_vouchers': self.meal_vouchers_checkbox.isChecked(),
        #     'transport_allowance': self.transport_allowance_checkbox.isChecked(),
            
        #     # Additional Information
        #     'education_level': self.education_level_combo.currentText(),
        #     'languages': self.languages_edit.text().strip(),
        #     'special_requirements': self.special_requirements_edit.toPlainText().strip(),
        #     'confidentiality': self.confidentiality_checkbox.isChecked(),
        #     'non_compete': self.non_compete_checkbox.isChecked(),
        # }
        
        # Pass data to controller (if method exists)
        if hasattr(self.controller, 'set_employee_data'):
            self.controller.set_employee_data(self.employee_data)
        
        log.info(f"Employee data collected (scrollable form): {len(self.employee_data)} fields")
        self.controller.next_step()

    # def clear_form(self):
    #     """Clear all form fields"""
    #     # Clear text fields
    #     for widget in [self.employee_name_edit, self.employee_egn_edit, self.employee_id_card_edit,
    #                   self.employee_phone_edit, self.employee_email_edit, self.birth_place_edit,
    #                   self.position_edit, self.department_edit, self.work_location_edit,
    #                   self.immediate_supervisor_edit, self.languages_edit]:
    #         widget.clear()
        
    #     # Clear text areas
    #     self.employee_address_edit.clear()
    #     self.special_requirements_edit.clear()
        
    #     # Reset spinboxes to defaults
    #     self.probation_period_spinbox.setValue(0)
    #     self.contract_duration_spinbox.setValue(0)
    #     self.notice_period_spinbox.setValue(1)
    #     self.salary_spinbox.setValue(760)
    #     self.bonus_percentage_spinbox.setValue(0)
    #     self.overtime_rate_spinbox.setValue(1.5)
    #     self.paid_vacation_days_spinbox.setValue(20)
        
    #     # Reset dates
    #     self.birth_date_edit.setDate(QDate.currentDate().addYears(-25))
    #     self.start_date_edit.setDate(QDate.currentDate())
        
    #     # Reset combos
    #     self.work_schedule_combo.setCurrentIndex(0)
    #     self.contract_type_combo.setCurrentIndex(0)
    #     self.education_level_combo.setCurrentIndex(0)
        
    #     # Uncheck checkboxes
    #     for checkbox in [self.health_insurance_checkbox, self.meal_vouchers_checkbox,
    #                     self.transport_allowance_checkbox, self.confidentiality_checkbox,
    #                     self.non_compete_checkbox]:
    #         checkbox.setChecked(False)
