import os, sys, pathlib
import docxtpl, yaml
from src.models.company_model import Company

class DocumentModel:
    def __init__(self, templates_path="data/document_templates"):
        self.templates_path = templates_path
        self.templates = self.scan_templates()
        self.tvarfiles = self.scan_template_varfiles()
        self._doc = None # docxtpl Document object
        self._doc_vars = [] # list of document variables
        self._doc_vars_metadata = {} # dict of document variables with metadata

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

    def get_document_vars(self, include_company: bool = False):
        """
        Returns the document variables that need to be filled.
        If include_company is True, it will also include company fields.
        """
        if not self._doc_vars:
            raise ValueError("No template selected or no variables found.")
        
        vars_to_fill = self._doc_vars.copy()
        
        if not include_company:
            company_fields_to_exclude = Company.get_docvars()
            for _, docvar in company_fields_to_exclude.items():
                if docvar in vars_to_fill:
                    vars_to_fill.remove(docvar)

        return vars_to_fill

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
            
        

    def get_document_vars_with_metadata(self, include_company: bool = False) -> dict:
        """
        Returns a dictionary of document variables with metadata.
        If include_company is True, it will also include company fields.
        """
        metadata = {}

        if not self._doc_vars:
            raise ValueError("No template selected or no variables found.")
        
        pretty_vars = {}

        vars_to_fill = self.get_document_vars(include_company)
        vars_metadata = self._doc_vars_metadata

        for pvar, props in vars_metadata.items():
            if props['multilang']:
                for lang in ['BG', 'EN']:
                    pvarlang = pvar + '_' + lang
                    if pvarlang in vars_to_fill:
                        pretty_vars[pvarlang] = {'hr_label' : props['hr_label'],
                                                  'type' : props['multilang_type'],
                                                  'concern': props['concern']}
            else:
                if pvar in vars_to_fill:
                    pretty_vars[pvar] = {'hr_label' : props['hr_label'], 
                                         'type' : 'string_probably',
                                         'concern' : props['concern']
                                         }
        
        return pretty_vars



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