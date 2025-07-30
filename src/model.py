
class DogovorinatorModel:
    def __init__(self, db):
        self.db = db
        self.selected_company = None
        self.employee_data = {}
        self.selected_contract_type = None
        # self.db.insert_example_entry()  # Insert an example entry on initialization
        # self.db.remove_example_entry()
        # for i in range(3):
        #     self.db.insert_company(name=f"Company {i}", vat_number=f"BG{i}", address=f"Address {i}")
        self.companies = self.db.fetch_all_companies()

    def add_company(self, name, vat_number, address):
        self.db.insert_company(name, vat_number, address)

    def get_companies(self):
        return self.companies
    
    def set_selected_company(self, company):
        self.selected_company = company
        print(f"Selected company set to: {company}")

    def set_selected_contract_type(self, contract_type):
        self.selected_contract_type = contract_type
        print(f"Selected contract type set to: {contract_type}")

    def set_employee_data(self, employee_data):
        self.employee_data = employee_data
        print(f"Employee data set to: {employee_data}")

if __name__ == "__main__":
    from src.db import DogovorinatorDatabase
    # Example usage
    db = DogovorinatorDatabase()
    model = DogovorinatorModel(db)
    print(model.get_companies())  # Should print the example company inserted during initialization
    db.close()