import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PySide6.QtCore import Qt

from src.controller import AppController
from src.logger import DogovLogger

log = DogovLogger.get_logger()

def main():
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = QMainWindow()
    main_window.setWindowTitle("Генератор на трудови договори")
    main_window.setMinimumSize(800, 600)
    main_window.resize(1000, 700)
    
    # Create the stacked widget to hold different views
    stacked_widget = QStackedWidget()
    main_window.setCentralWidget(stacked_widget)
    
    # Create controller with the stacked widget
    controller = AppController(stacked_widget)
    
    # Show main window
    main_window.show()
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
