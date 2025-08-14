import os, sys, pathlib
import docxtpl, yaml
from src.models.company_model import Company
from src.logger import DogovLogger

log = DogovLogger.get_logger()

class DocumentModel:
    def __init__(self, templates_path="data/document_templates"):
        self.templates_path = templates_path
        self.templates = self.scan_templates()
        self.tvarfiles = self.scan_template_varfiles()
        self._doc = None # docxtpl Document object
        self._doc_vars = [] # list of document variables
        self._doc_vars_metadata = {} # dict of document variables with metadata
        self._entry_vars = {}

    def scan_templates(self):
        """
        Scans the document templates directory and returns a list of template names without extensions.
        """
        return [os.path.splitext(f)[0] for f in os.listdir(self.templates_path) if f.endswith(".docx")]
    
    def scan_template_varfiles(self):
        """
        Scans the document templates directory and returns a list of template variable files without extensions.
        """
        return [os.path.splitext(f)[0] for f in os.listdir(self.templates_path) if f.endswith(".yaml")]

    def render_document(self, context):
        if not self._doc:
            raise ValueError("No template selected.")
        self._doc.render(context)

    def save_document(self):
        if not self._doc:
            raise ValueError("No template selected.")
        self._doc.save('RenderedContract.docx')

    def load_template(self, template: str):
        """
        Loads the specified template and extracts its document variables.
        """
        
        self._selected_template = template

        if template not in self.templates:
            raise ValueError(f"Template {template} not found.")
        
        template_file = f"{self.templates_path}/{template}.docx"
        
        if not os.path.exists(template_file):
            raise FileNotFoundError(f"Template file {template_file} does not exist.")
        
        self._doc = docxtpl.DocxTemplate(template_file)
        self._doc_vars = self._doc.get_undeclared_template_variables()
        
        if not self._doc_vars:
            raise ValueError("No document variables found in the template.")

    def load_template_metadata(self, template: str):
        """
        Loads metadata for the given template from a YAML file.
        """
        metadata_file = f"{self.templates_path}/{template}.yaml"
        
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as file:
                yamldict = yaml.safe_load(file)
                self._doc_vars_metadata = yamldict['vars']
            
        
    def set_company_data(self, company):
        company_dict = {
            "CMP_NAME_BG": company.name_bg,
            "CMP_NAME_EN": company.name_en,
            "CMP_BULSTAT": company.bulstat,
            "CMP_ADDR_BG": company.address_bg,
            "CMP_ADDR_EN": company.address_en,
            "CMP_REPR_EN": company.repr_en,
            "CMP_REPR_BG": company.repr_bg
        }
        self._entry_vars.update(company_dict)

    def validate_set_entry_vars(self, entered_vars: dict):
        """
        Validates and sets the document variables.
        """
        if not vars:
            raise ValueError("Document variables cannot be empty.")

        for entered, value in entered_vars.items():
            if entered in self._doc_vars_metadata.keys():
                if self._doc_vars_metadata[entered]['multilang']:
                    if self._doc_vars_metadata[entered]['multilang_type'] == 'date':
                        bgkey = f"{entered}_BG"
                        enkey = f"{entered}_EN"
                        # format date for bulgarian locale
                        bgdate = value.toString("dd.MM.yyyy")
                        endate = value.toString("dd MMM yyyy")
                        self._entry_vars[bgkey] = bgdate
                        self._entry_vars[enkey] = endate
                    else:
                        log.info(f"multilang var {entered} passed without explicit multiple languages")
                else:
                    self._entry_vars[entered] = value
            else:
                self._entry_vars[entered] = value
                    

    def get_current_entry_vars(self) -> dict:
        """
        Returns the current entry variables.
        """
        return self._entry_vars

    @property
    def selected_template(self) -> str:
        return self._selected_template

    @selected_template.setter
    def selected_template(self, template: str):
        self.load_template(template)
        self.load_template_metadata(template)

if __name__ == "__main__":
    # Example usage
    doc_model = DocumentModel()
    print("Available templates:", doc_model.templates)
    doc_model.selected_template = doc_model.templates[0]
    doc_vars_to_fill = doc_model.get_document_vars_with_metadata()
    for k,v in doc_vars_to_fill.items():
        print(f"{k}: {v}")