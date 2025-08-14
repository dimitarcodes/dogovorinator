from src.views.abstract_view import AbstractView
from src.logger import DogovLogger

from PySide6.QtWidgets import (QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
                              QLineEdit, QFormLayout, QDateEdit, QComboBox,
                              QGroupBox, QFrame, QTextEdit, QSpinBox, 
                              QScrollArea, QWidget, QCheckBox, QDoubleSpinBox,
                              QCompleter, QSizePolicy)
from PySide6.QtCore import Qt, QDate, QStringListModel
from PySide6.QtGui import QFont

log = DogovLogger.get_logger()

class TemporaryContractView(AbstractView):

    def _init_logic(self):
        self.all_countries = self.controller.get_all_countries()
        self.form_widgets = {}
    
    def _build_gui(self):
        # Title
        title_label = QLabel("Въведете данни за договора:")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Create scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        # Create scrollable widget
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)

        # Employee Personal Information Section
        personal_info_frame = QGroupBox("Лични данни на служителя")
        personal_layout = QVBoxLayout()
        personal_info_frame.setLayout(personal_layout)

        

        employee_name_box = QGroupBox("Имена на служителя")
        name_box_layout = QHBoxLayout()
        employee_name_box.setLayout(name_box_layout)

        #make name_box_layout not expand
        employee_name_box.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)


        employee_name_en_edit = QLineEdit()
        employee_name_bg_edit = QLineEdit()
        name_box_layout.addWidget(QLabel("Български:"))
        name_box_layout.addWidget(employee_name_bg_edit)
        name_box_layout.addWidget(QLabel("Английски:"))
        name_box_layout.addWidget(employee_name_en_edit)

        self.form_widgets['MPL_NAME_EN'] = employee_name_en_edit
        self.form_widgets['MPL_NAME_BG'] = employee_name_bg_edit


        personal_layout.addWidget(employee_name_box)

        employee_passport_box = QGroupBox("Паспорт на служителя")
        passport_box_layout = QFormLayout()
        passport_box_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        employee_passport_box.setLayout(passport_box_layout)

        date_of_birth_edit = QDateEdit()
        date_of_birth_edit.setCalendarPopup(True)
        date_of_birth_edit.setDate(QDate.currentDate().addYears(-25))
        passport_box_layout.addRow("Дата на раждане:", date_of_birth_edit)

        self.form_widgets['MPL_DOB'] = date_of_birth_edit

        country_of_origin_combo = QComboBox()
        country_of_origin_combo.setEditable(True)
        country_of_origin_combo.addItems(self.all_countries)

        coo_completer = QCompleter(self.all_countries, country_of_origin_combo)
        coo_completer.setCaseSensitivity(Qt.CaseInsensitive)
        coo_completer.setFilterMode(Qt.MatchContains)
        country_of_origin_combo.setCompleter(coo_completer)
        country_of_origin_combo.setCurrentText("Изберете държава")
        # passport_box_layout.addWidget(country_of_origin_combo)
        passport_box_layout.addRow("Държава:", country_of_origin_combo)

        self.form_widgets['MPL_CTZN'] = country_of_origin_combo

        date_of_expiry_edit = QDateEdit()
        date_of_expiry_edit.setCalendarPopup(True)
        date_of_expiry_edit.setDate(QDate.currentDate().addYears(1))
        passport_box_layout.addRow("Дата на изтичане:", date_of_expiry_edit)

        self.form_widgets['MPL_PPVD'] = date_of_expiry_edit

        date_of_issue_edit = QDateEdit()
        date_of_issue_edit.setCalendarPopup(True)
        date_of_issue_edit.setDate(QDate.currentDate())
        passport_box_layout.addRow("Дата на издаване:", date_of_issue_edit)

        self.form_widgets['MPL_PPID'] = date_of_issue_edit

        passport_number_edit = QLineEdit()
        passport_number_edit.setPlaceholderText("Номер на паспорт")
        passport_box_layout.addRow("Номер на паспорт:", passport_number_edit)

        self.form_widgets['MPL_PPN'] = passport_number_edit

        social_number_edit = QLineEdit()
        social_number_edit.setPlaceholderText("9907021234")
        passport_box_layout.addRow("ЕГН/ЛНЧ:", social_number_edit)

        self.form_widgets['MPL_IDN'] = social_number_edit

        personal_layout.addWidget(employee_passport_box)
        

        ###########################################################################################
        # Contract Details Frame

        contract_details_frame = QGroupBox("Данни за договора")
        contract_details_layout = QFormLayout()
        contract_details_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        contract_details_frame.setLayout(contract_details_layout)

        contract_number_edit = QLineEdit()
        contract_number_edit.setPlaceholderText("Номер на договора")
        contract_details_layout.addRow("Номер на договора:", contract_number_edit)

        self.form_widgets['CON_NUM'] = contract_number_edit

        contract_date_edit = QDateEdit()
        contract_date_edit.setCalendarPopup(True)
        contract_date_edit.setDate(QDate.currentDate())
        contract_details_layout.addRow("Дата на договора:", contract_date_edit)

        self.form_widgets['CON_DATE'] = contract_date_edit

        contract_sign_place_edit = QLineEdit()
        contract_sign_place_edit.setPlaceholderText("Място на подписване")
        contract_details_layout.addRow("Място на подписване:", contract_sign_place_edit)

        self.form_widgets['SIGN_PLACE'] = contract_sign_place_edit

        contract_len_edit = QSpinBox()
        contract_len_edit.setRange(1, 60)
        contract_len_edit.setSuffix(" месеца")
        contract_details_layout.addRow("Срок на договора:", contract_len_edit)

        self.form_widgets['CON_LEN'] = contract_len_edit

        contract_sign_date_edit = QDateEdit()
        contract_sign_date_edit.setCalendarPopup(True)
        contract_sign_date_edit.setDate(QDate.currentDate())
        contract_details_layout.addRow("Дата на подписване:", contract_sign_date_edit)

        self.form_widgets['SIGN_DATE'] = contract_sign_date_edit

        contract_start_date_edit = QDateEdit()
        contract_start_date_edit.setCalendarPopup(True)
        contract_start_date_edit.setDate(QDate.currentDate())
        contract_details_layout.addRow("Дата на започване:", contract_start_date_edit)

        self.form_widgets['CON_ST_DATE'] = contract_start_date_edit

        contract_end_date_edit = QDateEdit()
        contract_end_date_edit.setCalendarPopup(True)
        contract_end_date_edit.setDate(QDate.currentDate())
        contract_details_layout.addRow("Дата на приключване:", contract_end_date_edit)

        self.form_widgets['CON_END_DATE'] = contract_end_date_edit

        contract_work_start_edit = QDateEdit()
        contract_work_start_edit.setCalendarPopup(True)
        contract_work_start_edit.setDate(QDate.currentDate())
        contract_details_layout.addRow("Дата на постъпване на работа:", contract_work_start_edit)

        self.form_widgets['CON_ST_WORK_DATE'] = contract_work_start_edit


        ###########################################################################################
        # Position and Work Details Frame

        work_details_frame = QGroupBox("Данни за длъжността и работата")
        work_layout = QFormLayout()
        work_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        work_details_frame.setLayout(work_layout)
        
        job_pos_edit = QLineEdit()
        job_pos_edit.setPlaceholderText("Длъжност")
        work_layout.addRow("Длъжност:", job_pos_edit)

        self.form_widgets['JOB_POS'] = job_pos_edit

        job_dep_edit = QLineEdit()
        job_dep_edit.setPlaceholderText("Казино")
        work_layout.addRow("Отдел:", job_dep_edit)
        self.form_widgets['JOB_DEP'] = job_dep_edit

        job_loc_edit = QLineEdit()
        job_loc_edit.setPlaceholderText("гр. Варна, хотел Интернационал")
        work_layout.addRow("Място на работа:", job_loc_edit)
        self.form_widgets['JOB_WORKPLACE'] = job_loc_edit
        
        job_salary_usd_edit = QLineEdit()
        job_salary_usd_edit.setPlaceholderText("700")
        work_layout.addRow("Нетно възнаграждение в USD:", job_salary_usd_edit)
        self.form_widgets['JOB_SALARY_USD'] = job_salary_usd_edit

        job_salary_bgn_edit = QLineEdit()
        job_salary_bgn_edit.setPlaceholderText("1050")
        work_layout.addRow("Брутно възнагражение в BGN:", job_salary_bgn_edit)
        self.form_widgets['JOB_SALARY_BGN'] = job_salary_bgn_edit


        scroll_layout.addWidget(personal_info_frame)
        scroll_layout.addWidget(contract_details_frame)
        scroll_layout.addWidget(work_details_frame)

        scroll_layout.addStretch()  # Add stretch to push content to the top


        # Set scroll widget
        scroll_area.setWidget(scroll_widget)
        
        # Navigation frame
        nav_layout = QHBoxLayout()

        back_button = QPushButton("Назад")
        back_button.clicked.connect(self.controller.previous_step)

        start_button = QPushButton("Начало")
        start_button.clicked.connect(self.controller.go_to_start)

        next_button = QPushButton("Напред")
        next_button.clicked.connect(self._go_next)

        nav_layout.addWidget(back_button)
        nav_layout.addWidget(start_button)
        nav_layout.addStretch()
        nav_layout.addWidget(next_button)

        nav_frame = QFrame()
        nav_frame.setLayout(nav_layout)
        
        # Add all widgets to main layout
        self.main_layout.addWidget(title_label)
        self.main_layout.addWidget(scroll_area)  # Add the scroll area instead of individual frames
        self.main_layout.addWidget(nav_frame)
    
    def populate_forms(self):
        pass

    def _go_next(self):
        """Validate form and proceed to next step"""

        # log.info("Proceeding to next step with form data:")
        # for key, widget in self.form_widgets.items():
        #     if isinstance(widget, QDateEdit):
        #         log.info(f"{key}: {widget.date().toString(Qt.DateFormat.ISODate)}")
        #     elif isinstance(widget, QLineEdit):
        #         log.info(f"{key}: {widget.text()}")
        #     elif isinstance(widget, QComboBox):
        #         log.info(f"{key}: {widget.currentText()}")

        entered_vars = {}
        for key, widget in self.form_widgets.items():
            if isinstance(widget, QDateEdit):
                entered_vars[key] = widget.date()
            elif isinstance(widget, QLineEdit):
                entered_vars[key] = widget.text()
            elif isinstance(widget, QComboBox):
                entered_vars[key] = widget.currentText()
    
        self.controller.set_entered_vars(entered_vars)
