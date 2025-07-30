from src.views.selectCompanyView import SelectCompanyView
from src.views.selectContractTypeView import SelectContractTypeView
from src.views.finalPageView import FinalPageView
from src.views.fillOutContractFormView import filloutContractFormView

class  AppController():

    def __init__(self, model, root):
        self.model = model
        self.root = root
        
        self.current_view = 0

        self.views = [
            # StartPage(root),,
            SelectCompanyView(root),
            SelectContractTypeView(root),
            filloutContractFormView(root),
            FinalPageView(root)
        ]

        [view.set_controller(self) for view in self.views]

        self.show_view(self.current_view)
    
    def get_companies(self):
        return self.model.get_companies()
    
    def show_view(self, requested_view_number:int):
        
        for i, view in enumerate(self.views):
            if i != requested_view_number:
                print('hiding: ', i)
                view.hide()
        
        self.current_view = requested_view_number
        self.views[self.current_view].show()
    
    def next_step(self):
        self.show_view(self.current_view+1)

    def prev_step(self):
        self.show_view(self.current_view-1)
    
    def set_selected_company(self, company):
        self.model.set_selected_company(company)
        print(f"Selected company set to: {company}")
    
    def set_selected_contract_type(self, contract_type):
        self.model.set_selected_contract_type(contract_type)
        print(f"Selected contract type set to: {contract_type}")
    
    def set_employee_data(self, employee_data):
        self.model.set_employee_data(employee_data)