import tkinter
from tkinter import ttk
import sv_ttk

from src.logger import DogovLogger
from src.views import *
from src.models import *
from src.db import DogovorinatorDatabase

log = DogovLogger.get_logger()
class AppController():

    def __init__(self):
        self.app = tkinter.Tk()
        sv_ttk.set_theme("light")  # Set the theme to light
        
        self.app.title("Генератор на трудови договори")
        self.app.geometry("800x600")

        # Initialize MVC components
        self.db = DogovorinatorDatabase()
        self.CompanyModel = CompanyModel(self.db)
        self.DocumentModel = DocumentModel(templates_path="data/document_templates")
        self.EmployeeModel = EmployeeModel()

        self.current_view = 0

        self.views = [
            # StartPage(root),,
            SelectCompanyView(self.app, self),
            SelectContractTypeView(self.app, self),
            ContractDetailsFormView(self.app, self),
            ReviewSubmissionsView(self.app, self)
        ]
        
        self.show_view(self.current_view)
    
    def run(self):
        self.app.mainloop()

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
            del self.company_form_view
            log.info("Company form popup destroyed.")
        else:
            log.warning("No company form popup to destroy.")

    def add_company_dialog(self):
        """ Opens a dialog to add a new company. """
        log.info("Opening company form popup for adding a new company.")
        self.company_form_view = CompanyFormPopupView(self.app, self)

    def edit_company_dialog(self, company: Company):
        """ Opens a dialog to edit an existing company. """
        log.info(f"Opening company form popup for editing company: {company}")
        self.company_form_view = CompanyFormPopupView(self.app, self, company)

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
        
    def show_view(self, requested_view_number:int):
        
        log_msg = f'hiding: {[i for i,_ in enumerate(self.views) if i!=requested_view_number]}'
        log.info(log_msg)
        
        for i,view in enumerate(self.views):
            if i!=requested_view_number:
                view.hide()

        self.current_view = requested_view_number
        self.views[self.current_view].show()
    
    def next_step(self):
        self.show_view(self.current_view+1)

    def prev_step(self):
        self.show_view(self.current_view-1)
    
    def set_selected_company(self, company):
        self.CompanyModel.selected_company = company
        log_msg = f'Selected company set to: {company}'
        log.info(log_msg)
    
    def get_available_templates(self):
        return self.DocumentModel.templates
    
    def set_selected_contract_template(self, contract_template):
        self.DocumentModel.selected_template = contract_template
        log.info(f"Selected contract template set to: {self.DocumentModel.selected_template}")

    def set_employee_data(self, employee_data):
        self.EmployeeModel.selected_employee = Employee(**employee_data)