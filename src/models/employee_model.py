from src.logger import DogovLogger

log = DogovLogger.get_logger()
class EmployeeModel:
    def __init__(self):
        self.employees = []

    def get_employee_list(self):
        return self.employees
