from PySide6.QtWidgets import QStackedWidget, QMessageBox
from PySide6.QtCore import Qt

from src.logger import DogovLogger
from src.views.select_company_view import SelectCompanyView
from src.views.select_contract_type_view import SelectContractTypeView
from src.views.contract_details_form_view import ContractDetailsFormView
from src.views.contract_details_form_scrollable_view import ContractDetailsFormScrollableView
from src.views.review_submissions_view import ReviewSubmissionsView
from src.models import *
from src.db import DogovorinatorDatabase

log = DogovLogger.get_logger()

class AppController:
    def __init__(self, stacked_widget: QStackedWidget):
        self.stacked_widget = stacked_widget
        
        # Initialize MVC components (same as tkinter version)
        self.db = DogovorinatorDatabase()
        self.CompanyModel = CompanyModel(self.db)
        self.DocumentModel = DocumentModel(templates_path="data/document_templates")
        self.EmployeeModel = EmployeeModel()

        self.current_view_index = 0
        self.company_form_view = None

        # Create views
        self.views = [
            SelectCompanyView(self.stacked_widget, self),
            SelectContractTypeView(self.stacked_widget, self),
            ContractDetailsFormScrollableView(self.stacked_widget, self),
            ReviewSubmissionsView(self.stacked_widget, self)
        ]
        
        # Add views to stacked widget
        for view in self.views:
            self.stacked_widget.addWidget(view)
        
        self.show_view(self.current_view_index)

    def get_companies(self):
        return self.CompanyModel.get_companies()
    
    def update_company(self, company: Company):
        """ Update an existing company in the database. """
        if company.id is None:
            raise ValueError("Company must have an id to be updated.")
        
        self.CompanyModel.edit_company(company)
        self.views[0].reload_treeview()
        log.info(f"Company updated: {company}")
        return company

    def destroy_company_form(self):
        """ Destroys the company form popup if it exists. """
        if self.company_form_view:
            self.company_form_view.close()
            self.company_form_view = None
            log.info("Company form popup destroyed.")
        else:
            log.warning("No company form popup to destroy.")

    def add_company_dialog(self):
        """ Opens a dialog to add a new company. """
        log.info("Opening company form popup for adding a new company.")
        from src.views.company_form_popup_view import CompanyFormPopupView
        self.company_form_view = CompanyFormPopupView(self.stacked_widget, self)
        self.company_form_view.show()

    def edit_company_dialog(self, company: Company):
        """ Opens a dialog to edit an existing company. """
        log.info(f"Opening company form popup for editing company: {company}")
        from src.views.company_form_popup_view import CompanyFormPopupView
        self.company_form_view = CompanyFormPopupView(self.stacked_widget, self, company)
        self.company_form_view.show()

    def add_company(self, company: Company) -> Company:
        self.CompanyModel.add_company(company)
        self.views[0].reload_treeview()  # Reload the treeview in the SelectCompanyView
        log.info(f"Company added: {company}")
        return company
    
    def remove_company(self, company: Company):
        try:
            self.CompanyModel.remove_company(company)
            log.info(f"Company removed: {company}")
            self.views[0].reload_treeview()  # Reload the treeview in the SelectCompanyView
            return True
        except Exception as e:
            log.error(f"Error removing company: {e}")
            return False
        
    def show_view(self, requested_view_index: int):
        log_msg = f'Switching to view {requested_view_index}'
        log.info(log_msg)
        
        self.current_view_index = requested_view_index
        self.stacked_widget.setCurrentIndex(self.current_view_index)
    
    def next_step(self):
        if self.current_view_index < len(self.views) - 1:
            self.show_view(self.current_view_index + 1)
        else:
            log.info("Already at the last view")
    
    def previous_step(self):
        if self.current_view_index > 0:
            self.show_view(self.current_view_index - 1)
        else:
            log.info("Already at the first view")
    
    def go_to_start(self):
        self.show_view(0)

    def set_selected_company(self, company):
        """Set the selected company for contract generation"""
        self.selected_company = company
        log.info(f"Selected company: {company.name}")

    def get_selected_company(self):
        """Get the currently selected company"""
        return getattr(self, 'selected_company', None)

    def set_selected_contract_type(self, contract_type):
        """Set the selected contract type"""
        self.selected_contract_type = contract_type
        log.info(f"Selected contract type: {contract_type}")

    def get_selected_contract_type(self):
        """Get the currently selected contract type"""
        return getattr(self, 'selected_contract_type', None)

    def set_employee_data(self, employee_data):
        """Set the employee data for contract generation"""
        self.employee_data = employee_data
        log.info(f"Employee data set: {employee_data}")
        self.views[3]._update_review_text()  # Update review view with new employee data
    
    def get_employee_data(self):
        """Get the currently set employee data"""
        return getattr(self, 'employee_data', None)