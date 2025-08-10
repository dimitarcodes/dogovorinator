import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QDate

from src.controller import AppController
from src.models.entities import Company

# Create QApplication instance for testing (required for Qt widgets)
@pytest.fixture(scope="session")
def qapp():
    """Create QApplication instance for testing Qt widgets"""
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
    yield app
    # Don't quit the app here as it might be used by other tests

@pytest.fixture(autouse=True)
def mock_message_boxes():
    """Auto-mock all QMessageBox methods to prevent modal dialogs during testing"""
    with patch('src.views.abstract_view.QMessageBox') as mock_msgbox_class, \
         patch('src.controller.QMessageBox') as mock_msgbox_controller, \
         patch('PySide6.QtWidgets.QMessageBox') as mock_msgbox_global:
        
        # Mock the class-level methods for all patches
        for mock_msgbox in [mock_msgbox_class, mock_msgbox_controller, mock_msgbox_global]:
            mock_msgbox.question.return_value = QMessageBox.Yes
            mock_msgbox.warning.return_value = None
            mock_msgbox.information.return_value = None
            mock_msgbox.critical.return_value = None
            mock_msgbox.Yes = QMessageBox.Yes
            mock_msgbox.No = QMessageBox.No
            mock_msgbox.Warning = QMessageBox.Warning
            mock_msgbox.Information = QMessageBox.Information
            
            # Mock instance methods
            mock_msgbox_instance = Mock()
            mock_msgbox_instance.exec.return_value = None
            mock_msgbox_instance.setIcon.return_value = None
            mock_msgbox_instance.setWindowTitle.return_value = None
            mock_msgbox_instance.setText.return_value = None
            mock_msgbox.return_value = mock_msgbox_instance
        
        yield mock_msgbox_class

@pytest.fixture
def mock_database():
    """Mock database for testing"""
    with patch('src.controller.DogovorinatorDatabase') as mock_db:
        yield mock_db.return_value

@pytest.fixture
def mock_models():
    """Mock all model dependencies"""
    with patch('src.controller.CompanyModel') as mock_company, \
         patch('src.controller.DocumentModel') as mock_document, \
         patch('src.controller.EmployeeModel') as mock_employee:
        
        # Setup mock companies
        mock_companies = [
            Company(id=1, name="Test Company 1", vat_number="123456789", address="Test Address 1"),
            Company(id=2, name="Test Company 2", vat_number="987654321", address="Test Address 2")
        ]
        mock_company.return_value.get_companies.return_value = mock_companies
        
        yield {
            'company': mock_company.return_value,
            'document': mock_document.return_value,
            'employee': mock_employee.return_value
        }

@pytest.fixture
def stacked_widget(qapp):
    """Create QStackedWidget for testing"""
    return QStackedWidget()

@pytest.fixture
def controller(qapp, stacked_widget, mock_database, mock_models):
    """Create AppController instance for testing"""
    return AppController(stacked_widget)

class TestAppController:
    """Tests for AppController"""
    
    def test_controller_initialization(self, controller, stacked_widget):
        """Test that controller initializes properly"""
        assert controller.stacked_widget is stacked_widget
        assert controller.current_view_index == 0
        assert len(controller.views) == 4
        assert controller.company_form_view is None
    
    def test_get_companies(self, controller, mock_models):
        """Test getting companies from model"""
        # Reset call count since get_companies was called during initialization
        mock_models['company'].get_companies.reset_mock()
        
        companies = controller.get_companies()
        assert len(companies) == 2
        assert companies[0].name == "Test Company 1"
        mock_models['company'].get_companies.assert_called_once()
    
    def test_show_view(self, controller):
        """Test view switching"""
        controller.show_view(1)
        assert controller.current_view_index == 1
        assert controller.stacked_widget.currentIndex() == 1
    
    def test_next_step(self, controller):
        """Test navigation to next step"""
        initial_index = controller.current_view_index
        controller.next_step()
        assert controller.current_view_index == initial_index + 1
    
    def test_next_step_at_last_view(self, controller):
        """Test next step when already at last view"""
        controller.current_view_index = len(controller.views) - 1
        last_index = controller.current_view_index
        controller.next_step()
        assert controller.current_view_index == last_index  # Should stay the same
    
    def test_previous_step(self, controller):
        """Test navigation to previous step"""
        controller.current_view_index = 2
        controller.previous_step()
        assert controller.current_view_index == 1
    
    def test_previous_step_at_first_view(self, controller):
        """Test previous step when already at first view"""
        controller.current_view_index = 0
        controller.previous_step()
        assert controller.current_view_index == 0  # Should stay the same
    
    def test_go_to_start(self, controller):
        """Test going to start view"""
        controller.current_view_index = 2
        controller.go_to_start()
        assert controller.current_view_index == 0
    
    def test_set_and_get_selected_company(self, controller):
        """Test setting and getting selected company"""
        company = Company(id=1, name="Test Company", vat_number="123456789", address="Test Address")
        controller.set_selected_company(company)
        assert controller.get_selected_company() == company
    
    def test_set_and_get_selected_contract_type(self, controller):
        """Test setting and getting selected contract type"""
        contract_type = "permanent"
        controller.set_selected_contract_type(contract_type)
        assert controller.get_selected_contract_type() == contract_type
    
    def test_add_company(self, controller, mock_models):
        """Test adding a new company"""
        company = Company(name="New Company", vat_number="555666777", address="New Address")
        result = controller.add_company(company)
        
        assert result == company
        mock_models['company'].add_company.assert_called_once_with(company)
        # Should reload the treeview in the first view
        assert hasattr(controller.views[0], 'reload_treeview')
    
    def test_update_company(self, controller, mock_models):
        """Test updating an existing company"""
        company = Company(id=1, name="Updated Company", vat_number="123456789", address="Updated Address")
        result = controller.update_company(company)
        
        assert result == company
        mock_models['company'].edit_company.assert_called_once_with(company)
    
    def test_update_company_without_id(self, controller):
        """Test updating a company without ID raises error"""
        company = Company(name="Company Without ID", vat_number="123456789", address="Some Address")
        
        with pytest.raises(ValueError, match="Company must have an id to be updated"):
            controller.update_company(company)
    
    def test_remove_company_success(self, controller, mock_models):
        """Test successfully removing a company"""
        company = Company(id=1, name="Company to Remove", vat_number="123456789", address="Address to Remove")
        result = controller.remove_company(company)
        
        assert result is True
        mock_models['company'].remove_company.assert_called_once_with(company)
    
    def test_remove_company_failure(self, controller, mock_models):
        """Test handling failure when removing a company"""
        company = Company(id=1, name="Company to Remove", vat_number="123456789", address="Address to Remove")
        mock_models['company'].remove_company.side_effect = Exception("Database error")
        
        result = controller.remove_company(company)
        assert result is False
    
    @patch('src.views.company_form_popup_view.CompanyFormPopupView')
    def test_add_company_dialog(self, mock_popup, controller):
        """Test opening add company dialog"""
        controller.add_company_dialog()
        
        mock_popup.assert_called_once()
        assert controller.company_form_view is not None
    
    @patch('src.views.company_form_popup_view.CompanyFormPopupView')
    def test_edit_company_dialog(self, mock_popup, controller):
        """Test opening edit company dialog"""
        company = Company(id=1, name="Test Company", vat_number="123456789", address="Test Address")
        controller.edit_company_dialog(company)
        
        mock_popup.assert_called_once()
        assert controller.company_form_view is not None
    
    def test_destroy_company_form_with_existing_form(self, controller):
        """Test destroying company form when it exists"""
        mock_form = Mock()
        controller.company_form_view = mock_form
        
        controller.destroy_company_form()
        
        mock_form.close.assert_called_once()
        assert controller.company_form_view is None
    
    def test_destroy_company_form_without_existing_form(self, controller):
        """Test destroying company form when it doesn't exist"""
        controller.company_form_view = None
        
        # Should not raise any errors
        controller.destroy_company_form()
        assert controller.company_form_view is None
