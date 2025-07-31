import os, sys, pathlib
import docxtpl

class DocumentModel:
    def __init__(self, path="data/document_templates"):
        self.path = path
        self.templates = self.scan_templates()
        self.doc = None # docxtrpl Document object
        self.doc_vars = []

    def scan_templates(self):
        return [f for f in os.listdir(self.path) if f.endswith(".docx")]

    def select_template(self, template_name):
        if template_name not in self.templates:
            raise ValueError(f"Template {template_name} not found.")
        self.doc = docxtpl.DocxTemplate(f"{self.path}/{template_name}")
        self.doc_vars = self.doc.get_undeclared_template_variables()
    
    def render_document(self, context):
        if not self.doc:
            raise ValueError("No template selected.")
        self.doc.render(context)

    def save_document(self):
        if not self.doc:
            raise ValueError("No template selected.")
        self.doc.save('RenderedContract.docx')
