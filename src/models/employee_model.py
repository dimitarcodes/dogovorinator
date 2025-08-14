from src.logger import DogovLogger
import yaml

log = DogovLogger.get_logger()
class EmployeeModel:
    def __init__(self):
        self.bg_countries_dict = self.load_countries()
        self.en_countries_dict = self.load_countries()
        self.bg_all_countries_list = list(self.bg_countries_dict.values())
        self.en_all_countries_list = list(self.en_countries_dict.values())

    def load_countries(self, datapath="data/assets/", fname="countries_bg.yaml"):
        """ Load countries from a YAML file. """
        # check if file exists
        try:
            with open(f"{datapath}/{fname}", 'r', encoding='utf-8') as file:
                countries = yaml.safe_load(file)
                log.info(f"Loaded countries from {fname}")
                return countries
        except FileNotFoundError:
            log.error(f"File {fname} not found in {datapath}")
            return []
        except Exception as e:
            log.error(f"Error loading countries from {fname}: {e}")
            return []

    def get_employee_list(self):
        return self.employees
