from src.logger import DogovLogger
from src.views.select_company_view import SelectCompanyView
from src.views.select_contract_type_view import SelectContractTypeView
from src.views.review_submissions_view import ReviewSubmissionsView
from src.views.contract_details_form_view import ContractDetailsFormView

log = DogovLogger.get_logger()
class AppController():

    def __init__(self, model, root):
        
        self.model = model
        self.root = root
        
        self.current_view = 0

        self.views = [
            # StartPage(root),,
            SelectCompanyView(root, self),
            SelectContractTypeView(root, self),
            ContractDetailsFormView(root, self),
            ReviewSubmissionsView(root, self)
        ]

        # for view in self.views:
        #     view.controller = self

        self.show_view(self.current_view)
    
    def get_companies(self):
        return self.model.get_companies()
    
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
        self.model.set_selected_company(company)

        log_msg = f'Selected company set to: {company}'
        log.info(log_msg)
    
    def set_selected_contract_type(self, contract_type):
        self.model.set_selected_contract_type(contract_type)
        log.info(f"Selected contract type set to: {contract_type}")
    
    def set_employee_data(self, employee_data):
        self.model.set_employee_data(employee_data)