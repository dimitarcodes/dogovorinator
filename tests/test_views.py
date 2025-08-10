import pytest
import sys
from unittest.mock import MagicMock, patch, Mock
from PySide6.QtWidgets import QApplication, QStackedWidget, QMessageBox
from PySide6.QtTest import QTest
from PySide6.QtCore import Qt, QDate

from src.views.select_company_view import SelectCompanyView
from src.views.select_contract_type_view import SelectContractTypeView
from src.views.contract_details_form_view import ContractDetailsFormView
from src.views.contract_details_form_scrollable_view import ContractDetailsFormScrollableView
from src.views.review_submissions_view import ReviewSubmissionsView
from src.models.company_model import Company

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
    with patch('src.views.abstract_view.QMessageBox') as mock_msgbox_class, \
         patch('src.views.company_form_popup_view.QMessageBox') as mock_msgbox_popup, \
         patch('PySide6.QtWidgets.QMessageBox') as mock_msgbox_global:
        
        # Mock the class-level methods for all patches
        for mock_msgbox in [mock_msgbox_class, mock_msgbox_popup, mock_msgbox_global]:
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
def mock_controller():
    """Mock controller for testing views"""
    controller = Mock()
    controller.get_companies.return_value = [
        Company(id=1, name="Test Company 1", vat_number="123456789", address="Test Address 1"),
        Company(id=2, name="Test Company 2", vat_number="987654321", address="Test Address 2")
    ]
    controller.get_selected_company.return_value = Company(id=1, name="Test Company 1", vat_number="123456789", address="Test Address 1")
    controller.get_selected_contract_type.return_value = "permanent"
    controller.get_employee_data.return_value = {
        'name': 'John Doe',
        'egn': '1234567890',
        'position': 'Developer',
        'salary': 2000,
        'start_date': '2025-01-01'
    }
    return controller

@pytest.fixture
def parent_widget(qapp):
    """Create parent widget for testing"""
    return QStackedWidget()

class TestSelectCompanyView:
    """Tests for SelectCompanyView"""
    
    def test_view_initialization(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly"""
        view = SelectCompanyView(parent_widget, mock_controller)
        
        assert view._controller is mock_controller
        assert hasattr(view, 'companies_table')
        assert hasattr(view, 'title_label')
        assert hasattr(view, 'next_button')
    
    def test_reload_table(self, qapp, parent_widget, mock_controller):
        """Test reloading companies table"""
        view = SelectCompanyView(parent_widget, mock_controller)
        view.reload_table()
        
        # Check that table has correct number of rows
        assert view.companies_table.rowCount() == 2
        # Check that controller method was called
        mock_controller.get_companies.assert_called()
    
    def test_reload_treeview_compatibility(self, qapp, parent_widget, mock_controller):
        """Test that reload_treeview method works (compatibility)"""
        view = SelectCompanyView(parent_widget, mock_controller)
        # Should not raise any errors
        view.reload_treeview()
        assert view.companies_table.rowCount() == 2
    
    def test_select_company_with_selection(self, qapp, parent_widget, mock_controller):
        """Test selecting a company when row is selected"""
        view = SelectCompanyView(parent_widget, mock_controller)
        view.reload_table()
        
        # Simulate selecting first row
        view.companies_table.setCurrentCell(0, 0)
        company = view._select_company()
        
        assert company is not None
        assert company.name == "Test Company 1"
    
    def test_select_company_without_selection(self, qapp, parent_widget, mock_controller):
        """Test selecting a company when no row is selected"""
        view = SelectCompanyView(parent_widget, mock_controller)
        view.reload_table()
        
        # No selection made
        company = view._select_company()
        
        assert company is None
    
    def test_go_next_with_selection(self, qapp, parent_widget, mock_controller):
        """Test going to next step with company selected"""
        view = SelectCompanyView(parent_widget, mock_controller)
        view.reload_table()
        view.companies_table.setCurrentCell(0, 0)
        
        view._go_next()
        
        mock_controller.set_selected_company.assert_called_once()
        mock_controller.next_step.assert_called_once()
    
    def test_go_next_without_selection(self, qapp, parent_widget, mock_controller):
        """Test going to next step without company selected"""
        view = SelectCompanyView(parent_widget, mock_controller)
        view.reload_table()
        
        # Don't select any row
        view._go_next()
        
        # Should not proceed to next step
        mock_controller.set_selected_company.assert_not_called()
        mock_controller.next_step.assert_not_called()

class TestSelectContractTypeView:
    """Tests for SelectContractTypeView"""
    
    def test_view_initialization(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly"""
        view = SelectContractTypeView(parent_widget, mock_controller)
        
        assert view._controller is mock_controller
        assert hasattr(view, 'title_label')
        assert hasattr(view, 'contract_type1_button')
        assert hasattr(view, 'contract_type2_button')
    
    def test_select_permanent_contract(self, qapp, parent_widget, mock_controller):
        """Test selecting permanent contract type"""
        view = SelectContractTypeView(parent_widget, mock_controller)
        
        view._select_contract("permanent")
        
        mock_controller.set_selected_contract_type.assert_called_once_with("permanent")
        mock_controller.next_step.assert_called_once()
    
    def test_select_temporary_contract(self, qapp, parent_widget, mock_controller):
        """Test selecting temporary contract type"""
        view = SelectContractTypeView(parent_widget, mock_controller)
        
        view._select_contract("temporary")
        
        mock_controller.set_selected_contract_type.assert_called_once_with("temporary")
        mock_controller.next_step.assert_called_once()
    
    def test_back_button_functionality(self, qapp, parent_widget, mock_controller):
        """Test back button calls previous_step"""
        view = SelectContractTypeView(parent_widget, mock_controller)
        
        # Simulate back button click
        QTest.mouseClick(view.back_button, Qt.LeftButton)
        
        mock_controller.previous_step.assert_called_once()

class TestContractDetailsFormView:
    """Tests for ContractDetailsFormView"""
    
    def test_view_initialization(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly"""
        view = ContractDetailsFormView(parent_widget, mock_controller)
        
        assert view._controller is mock_controller
        assert hasattr(view, 'employee_name_edit')
        assert hasattr(view, 'employee_egn_edit')
        assert hasattr(view, 'position_edit')
        assert hasattr(view, 'salary_spinbox')
        assert hasattr(view, 'start_date_edit')
    
    def test_form_validation_empty_name(self, qapp, parent_widget, mock_controller):
        """Test form validation with empty name"""
        view = ContractDetailsFormView(parent_widget, mock_controller)
        
        # Fill other fields but leave name empty
        view.employee_egn_edit.setText("1234567890")
        view.position_edit.setText("Developer")
        
        view._go_next()
        
        # Should not proceed to next step
        mock_controller.next_step.assert_not_called()
    
    def test_form_validation_empty_egn(self, qapp, parent_widget, mock_controller):
        """Test form validation with empty EGN"""
        view = ContractDetailsFormView(parent_widget, mock_controller)
        
        # Fill other fields but leave EGN empty
        view.employee_name_edit.setText("John Doe")
        view.position_edit.setText("Developer")
        
        view._go_next()
        
        # Should not proceed to next step
        mock_controller.next_step.assert_not_called()
    
    def test_form_validation_empty_position(self, qapp, parent_widget, mock_controller):
        """Test form validation with empty position"""
        view = ContractDetailsFormView(parent_widget, mock_controller)
        
        # Fill other fields but leave position empty
        view.employee_name_edit.setText("John Doe")
        view.employee_egn_edit.setText("1234567890")
        
        view._go_next()
        
        # Should not proceed to next step
        mock_controller.next_step.assert_not_called()
    
    def test_successful_form_submission(self, qapp, parent_widget, mock_controller):
        """Test successful form submission with all fields filled"""
        view = ContractDetailsFormView(parent_widget, mock_controller)
        
        # Fill all required fields
        view.employee_name_edit.setText("John Doe")
        view.employee_egn_edit.setText("1234567890")
        view.position_edit.setText("Developer")
        view.salary_spinbox.setValue(2000)
        view.start_date_edit.setDate(QDate.currentDate())
        
        view._go_next()
        
        # Should proceed to next step and set employee data
        mock_controller.set_employee_data.assert_called_once()
        mock_controller.next_step.assert_called_once()
        
        # Check that data was collected correctly
        call_args = mock_controller.set_employee_data.call_args[0][0]
        assert call_args['name'] == "John Doe"
        assert call_args['egn'] == "1234567890"
        assert call_args['position'] == "Developer"
        assert call_args['salary'] == 2000

class TestContractDetailsFormScrollableView:
    """Tests for ContractDetailsFormScrollableView"""
    
    def test_view_initialization(self, qapp, parent_widget, mock_controller):
        """Test that scrollable view initializes properly"""
        view = ContractDetailsFormScrollableView(parent_widget, mock_controller)
        
        assert view._controller is mock_controller
        assert hasattr(view, 'employee_name_edit')
        assert hasattr(view, 'employee_egn_edit')
        assert hasattr(view, 'position_edit')
        assert hasattr(view, 'salary_spinbox')
        # Additional fields specific to scrollable form
        assert hasattr(view, 'employee_phone_edit')
        assert hasattr(view, 'department_edit')
        assert hasattr(view, 'contract_type_combo')
    
    def test_comprehensive_data_collection(self, qapp, parent_widget, mock_controller):
        """Test that all form fields are collected properly"""
        view = ContractDetailsFormScrollableView(parent_widget, mock_controller)
        
        # Fill required fields
        view.employee_name_edit.setText("John Doe")
        view.employee_egn_edit.setText("1234567890")
        view.position_edit.setText("Developer")
        view.employee_phone_edit.setText("+359888123456")
        view.department_edit.setText("IT Department")
        
        view._go_next()
        
        # Should collect comprehensive data
        mock_controller.set_employee_data.assert_called_once()
        call_args = mock_controller.set_employee_data.call_args[0][0]
        
        # Check that all expected fields are present
        expected_fields = ['name', 'egn', 'position', 'phone', 'department', 'salary', 
                          'start_date', 'contract_type', 'education_level']
        for field in expected_fields:
            assert field in call_args
    
    def test_clear_form_functionality(self, qapp, parent_widget, mock_controller):
        """Test clearing all form fields"""
        view = ContractDetailsFormScrollableView(parent_widget, mock_controller)
        
        # Fill some fields
        view.employee_name_edit.setText("Test Name")
        view.employee_egn_edit.setText("1234567890")
        view.salary_spinbox.setValue(3000)
        view.health_insurance_checkbox.setChecked(True)
        
        # Clear form
        view.clear_form()
        
        # Check that fields are cleared
        assert view.employee_name_edit.text() == ""
        assert view.employee_egn_edit.text() == ""
        assert view.salary_spinbox.value() == 760  # Default minimum wage
        assert not view.health_insurance_checkbox.isChecked()

class TestReviewSubmissionsView:
    """Tests for ReviewSubmissionsView"""
    
    def test_view_initialization(self, qapp, parent_widget, mock_controller):
        """Test that view initializes properly"""
        view = ReviewSubmissionsView(parent_widget, mock_controller)
        
        assert view._controller is mock_controller
        assert hasattr(view, 'title_label')
        assert hasattr(view, 'review_text')
        assert hasattr(view, 'generate_button')
    
    def test_update_review_text(self, qapp, parent_widget, mock_controller):
        """Test updating review text with selected data"""
        view = ReviewSubmissionsView(parent_widget, mock_controller)
        
        view._update_review_text()
        
        # Should call controller methods to get data
        mock_controller.get_selected_company.assert_called_once()
        mock_controller.get_selected_contract_type.assert_called_once()
        
        # Review text should contain company information
        review_text = view.review_text.toPlainText()
        assert "Test Company 1" in review_text
        assert "123456789" in review_text
        assert "Постоянен трудов договор" in review_text
    
    def test_show_method_updates_text(self, qapp, parent_widget, mock_controller):
        """Test that showing the view updates review text"""
        view = ReviewSubmissionsView(parent_widget, mock_controller)
        
        view.show()
        
        # Should have called methods to update review text
        mock_controller.get_selected_company.assert_called()
        mock_controller.get_selected_contract_type.assert_called()
    
    def test_generate_contract(self, qapp, parent_widget, mock_controller):
        """Test contract generation functionality"""
        view = ReviewSubmissionsView(parent_widget, mock_controller)
        
        # Should not raise any errors
        view._generate_contract()
        
        # This is currently a placeholder, so just check it doesn't crash
