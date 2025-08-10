import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt

from src.views.company_form_popup_view import CompanyFormPopupView
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

@pytest.fixture(autouse=True)
def mock_message_boxes():
    """Auto-mock all QMessageBox methods to prevent modal dialogs during testing"""
    with patch('src.views.company_form_popup_view.QMessageBox') as mock_msgbox_popup, \
         patch('src.views.abstract_view.QMessageBox') as mock_msgbox_class, \
         patch('PySide6.QtWidgets.QMessageBox') as mock_msgbox_global:
        
        # Mock the class-level methods for all patches
        for mock_msgbox in [mock_msgbox_popup, mock_msgbox_class, mock_msgbox_global]:
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
        
        yield mock_msgbox_popup

@pytest.fixture
def mock_controller():
    """Mock controller for testing company form"""
    controller = Mock()
    return controller

@pytest.fixture
def parent_widget(qapp):
    """Create parent widget for testing"""
    return QStackedWidget()

class TestCompanyFormPopupView:
    """Tests for CompanyFormPopupView"""
    
    def test_view_initialization_add_mode(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly in add mode"""
        view = CompanyFormPopupView(parent_widget, mock_controller)
        
        assert view.controller is mock_controller
        assert view.mode == "add"
        assert view.company is None
        assert view.isModal()
        assert "Добавяне на фирма" in view.windowTitle()
    
    def test_view_initialization_edit_mode(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly in edit mode"""
        company = Company(id=1, name="Test Company", vat_number="123456789", address="Test Address")
        view = CompanyFormPopupView(parent_widget, mock_controller, company)
        
        assert view.controller is mock_controller
        assert view.mode == "edit"
        assert view.company is company
        assert "Редактиране на фирма" in view.windowTitle()
    
    def test_form_fields_populated_in_edit_mode(self, qapp, parent_widget, mock_controller):
        """Test that form fields are populated when editing existing company"""
        company = Company(id=1, name="Test Company", vat_number="123456789", address="Test Address")
        
        # Mock Company.get_fields() to return expected fields
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller, company)
            
            # Check that fields are populated with company data
            assert view.company_form['name'].text() == "Test Company"
            assert view.company_form['vat_number'].text() == "123456789"
            assert view.company_form['address'].text() == "Test Address"
    
    def test_validate_company_form_valid_data(self, qapp, parent_widget, mock_controller):
        """Test form validation with valid data"""
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller)
            
            # Fill form with valid data
            view.company_form['name'].setText("Valid Company")
            view.company_form['vat_number'].setText("123456789")
            view.company_form['address'].setText("Valid Address")
            
            data = view._validate_company_form()
            
            assert data is not None
            assert data['name'] == "Valid Company"
            assert data['vat_number'] == "123456789"
            assert data['address'] == "Valid Address"
    
    def test_validate_company_form_empty_field(self, qapp, parent_widget, mock_controller):
        """Test form validation with empty required field"""
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller)
            
            # Fill only some fields, leave others empty
            view.company_form['name'].setText("Company Name")
            view.company_form['vat_number'].setText("123456789")
            view.company_form['address'].setText("")  # Empty field
            
            data = view._validate_company_form()
            
            assert data is None  # Should return None for invalid data
    
    def test_save_company_add_mode_success(self, qapp, parent_widget, mock_controller):
        """Test successfully saving a new company"""
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller)
            
            # Fill form with valid data
            view.company_form['name'].setText("New Company")
            view.company_form['vat_number'].setText("987654321")
            view.company_form['address'].setText("New Address")
            
            # Mock the accept method to prevent dialog from closing
            with patch.object(view, 'accept') as mock_accept:
                view._save_company()
                
                # Should call controller's add_company method
                mock_controller.add_company.assert_called_once()
                mock_accept.assert_called_once()
    
    def test_save_company_edit_mode_success(self, qapp, parent_widget, mock_controller):
        """Test successfully updating an existing company"""
        company = Company(id=1, name="Old Name", vat_number="123456789", address="Old Address")
        
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller, company)
            
            # Update form data
            view.company_form['name'].setText("Updated Name")
            view.company_form['vat_number'].setText("987654321")
            view.company_form['address'].setText("Updated Address")
            
            # Mock the accept method to prevent dialog from closing
            with patch.object(view, 'accept') as mock_accept:
                view._save_company()
                
                # Should call controller's update_company method
                mock_controller.update_company.assert_called_once()
                # Check that company object was updated
                assert company.name == "Updated Name"
                assert company.vat_number == "987654321"
                assert company.address == "Updated Address"
                mock_accept.assert_called_once()
    
    def test_save_company_validation_failure(self, qapp, parent_widget, mock_controller):
        """Test save company with validation failure"""
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller)
            
            # Leave required fields empty
            view.company_form['name'].setText("")
            view.company_form['vat_number'].setText("123456789")
            view.company_form['address'].setText("Some Address")
            
            view._save_company()
            
            # Should not call controller methods
            mock_controller.add_company.assert_not_called()
            mock_controller.update_company.assert_not_called()
    
    def test_save_company_exception_handling(self, qapp, parent_widget, mock_controller):
        """Test save company with exception from controller"""
        with patch.object(Company, 'get_fields', return_value=['name', 'vat_number', 'address']):
            view = CompanyFormPopupView(parent_widget, mock_controller)
            
            # Fill form with valid data
            view.company_form['name'].setText("Test Company")
            view.company_form['vat_number'].setText("123456789")
            view.company_form['address'].setText("Test Address")
            
            # Make controller raise an exception
            mock_controller.add_company.side_effect = Exception("Database error")
            
            view._save_company()
            
            # Should handle the exception gracefully
            mock_controller.add_company.assert_called_once()
    
    def test_reject_dialog(self, qapp, parent_widget, mock_controller):
        """Test rejecting/cancelling the dialog"""
        view = CompanyFormPopupView(parent_widget, mock_controller)
        
        # Mock the parent reject method to prevent dialog from closing
        with patch('PySide6.QtWidgets.QDialog.reject') as mock_super_reject:
            view.reject()
            
            # Should call destroy_company_form on controller
            mock_controller.destroy_company_form.assert_called_once()
            mock_super_reject.assert_called_once()
    
    def test_accept_dialog(self, qapp, parent_widget, mock_controller):
        """Test accepting the dialog"""
        view = CompanyFormPopupView(parent_widget, mock_controller)
        
        # Mock the parent accept method to prevent dialog from closing
        with patch('PySide6.QtWidgets.QDialog.accept') as mock_super_accept:
            view.accept()
            
            # Should call destroy_company_form on controller
            mock_controller.destroy_company_form.assert_called_once()
            mock_super_accept.assert_called_once()
