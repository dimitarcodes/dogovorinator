from src.logger import DogovLogger
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMessageBox, QFileDialog
from PySide6.QtCore import Qt
from abc import abstractmethod

class AbstractView(QWidget):
    def __init__(self, parent_widget, controller):
        super().__init__()
        self._parent_widget = parent_widget
        self._controller = controller
        
        # Set up main layout
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        
        self._init_logic()
        self._build_gui()
        self.hide()
    
    def _init_logic(self):
        # get necessary data from controller
        pass

    @abstractmethod
    def _build_gui(self):
        # build GUI elements (widgets)
        pass

    def show(self):
        """Show this view widget"""
        super().show()
    
    def hide(self):
        """Hide this view widget"""
        super().hide()

    @property
    def controller(self):
        """The controller responsible for communicating with model layer and managing views."""
        return self._controller
    
    @controller.setter
    def controller(self, ctrlr):
        self._controller = ctrlr

    def show_warning(self, title, message):
        """Show a warning message box"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def show_info(self, title, message):
        """Show an info message box"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

    def ask_yes_no(self, title, message):
        """Show a yes/no dialog and return True if Yes was clicked"""
        reply = QMessageBox.question(self, title, message, 
                                   QMessageBox.Yes | QMessageBox.No)
        return reply == QMessageBox.Yes
