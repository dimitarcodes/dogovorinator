from src.models.document_model import DocumentModel

def test_init():
    doc_model = DocumentModel(templates_path="data/document_templates")
    assert doc_model.templates == ["PermanentContractTemplate", "TemporaryContractTemplate"]

def test_scan_templates(monkeypatch):
    # Mock the os.listdir function to return a predefined list of files
    monkeypatch.setattr("os.listdir", lambda path: ["template1.docx", "template2.docx", "not_a_template.txt"])
    
    doc_model = DocumentModel()
    templates = doc_model.scan_templates()

    assert templates == ["template1", "template2"]

def test_select_template():
    doc_model = DocumentModel(templates_path="data/document_templates")
    doc_model.selected_template = "PermanentContractTemplate"

    assert doc_model._doc is not None
    assert doc_model._doc_vars  # Assuming doc has variables to be inserted
