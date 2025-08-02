import os, sys, pathlib
import docxtpl

class DocumentModel:
    def __init__(self, templates_path="data/document_templates"):
        self.templates_path = templates_path
        self.templates = self.scan_templates()
        self.doc = None # docxtrpl Document object
        self.doc_vars = []

    def scan_templates(self):
        """
        Scans the document templates directory and returns a list of template names without extensions.
        """
        return [os.path.splitext(f)[0] for f in os.listdir(self.templates_path) if f.endswith(".docx")]
    
    def render_document(self, context):
        if not self.doc:
            raise ValueError("No template selected.")
        self.doc.render(context)

    def save_document(self):
        if not self.doc:
            raise ValueError("No template selected.")
        self.doc.save('RenderedContract.docx')

    @property
    def selected_template(self) -> str:
        return self._selected_template

    @selected_template.setter
    def selected_template(self, template: str):
        if template not in self.templates:
            raise ValueError(f"Template {template} not found.")
        self._selected_template = template
        self._doc = docxtpl.DocxTemplate(f"{self.templates_path}/{template}.docx")
        self._doc_vars = self._doc.get_undeclared_template_variables()
