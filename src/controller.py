import tkinter
from tkinter import ttk
import sv_ttk

from src.logger import DogovLogger
from src.views import SelectCompanyView, SelectContractTypeView, ReviewSubmissionsView, ContractDetailsFormView
from src.models import CompanyModel, DocumentModel, EmployeeModel, Company, Employee
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
        
        # Update the company in the database
        # self.CompanyModel.remove_company(company)
        # self.CompanyModel.add_company(company)
        self.CompanyModel.edit_company(company)
        log.info(f"Company updated: {company}")
        return company

    def add_company(self, company: Company) -> Company:
        self.CompanyModel.add_company(company)
        log.info(f"Company added: {company}")
        return company
    
    def remove_company(self, company: Company):
        try:
            self.CompanyModel.remove_company(company)
            log.info(f"Company removed: {company}")
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
    
    def set_selected_contract_template(self, contract_template):
        self.DocumentModel.selected_template = contract_template
        log.info(f"Selected contract template set to: {contract_template}")

    def set_employee_data(self, employee_data):
        self.EmployeeModel.selected_employee = Employee(**employee_data)