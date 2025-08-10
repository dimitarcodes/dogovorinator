import os, sys, pathlib
import docxtpl
from src.models.entities import Company
class DocumentModel:
    def __init__(self, templates_path="data/document_templates"):
        self.templates_path = templates_path
        self.templates = self.scan_templates()
        self._doc = None # docxtpl Document object
        self._doc_vars = [] # list of document variables

    def scan_templates(self):
        """
        Scans the document templates directory and returns a list of template names without extensions.
        """
        return [os.path.splitext(f)[0] for f in os.listdir(self.templates_path) if f.endswith(".docx")]
    
    def render_document(self, context):
        if not self._doc:
            raise ValueError("No template selected.")
        self._doc.render(context)

    def save_document(self):
        if not self._doc:
            raise ValueError("No template selected.")
        self._doc.save('RenderedContract.docx')

    def get_document_vars(self, include_company: bool = False) -> list:
        """
        Returns the document variables that need to be filled.
        If include_company is True, it will also include company fields.
        """
        if not self._doc_vars:
            raise ValueError("No template selected or no variables found.")
        
        vars_to_fill = self._doc_vars.copy()
        
        if not include_company:
            company_fields_to_exclude = Company.get_docvar()
            for _, docvar in company_fields_to_exclude.items():
                if docvar in vars_to_fill:
                    vars_to_fill.remove(docvar)

        return vars_to_fill

    @property
    def selected_template(self) -> str:
        return self._selected_template

    @selected_template.setter
    def selected_template(self, template: str):
        if template not in self.templates:
            raise ValueError(f"Template {template} not found.")
        self._selected_template = template
        self._doc = docxtpl.DocxTemplate(f"{self.templates_path}/{template}.docx")
        self._doc_vars = list(self._doc.get_undeclared_template_variables())

if __name__ == "__main__":
    # Example usage
    doc_model = DocumentModel()
    print("Available templates:", doc_model.templates)
    doc_model.selected_template = doc_model.templates[0]
    doc_vars_to_fill = doc_model.get_document_vars(include_company=True)
    print("Document variables:", doc_vars_to_fill)
    doc_vars_to_fill = doc_model.get_document_vars(include_company=False)
    print("Document variables to fill:", doc_vars_to_fill)