from src.models.entities import Employee
from src.logger import DogovLogger

log = DogovLogger().get_logger()
class EmployeeModel:
    def __init__(self):
        self.employees = []

    def get_employee_list(self):
        return self.employees

    @property
    def selected_employee(self) -> Employee:
        return self._selected_employee
    
    @selected_employee.setter
    def selected_employee(self, employee: Employee):
        self._selected_employee = employee
        self.employees.append(employee)
    
    @selected_employee.getter
    def selected_employee(self) -> Employee:
        if not hasattr(self, '_selected_employee'):
            raise ValueError("No employee selected.")
        return self._selected_employee