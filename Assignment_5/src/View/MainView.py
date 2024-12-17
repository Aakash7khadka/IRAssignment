
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout,
    QMessageBox,
    QGridLayout
)

from PyQt5 import(
    QtGui
)

from PyQt5.QtGui import QColor, QPalette

from src.View.HeaderView import HeaderView
from src.View.SearchView import SearchView
from src.View.ClusterView import ClusterView
from src.Controller.MainController import MainController
from src.View.StackedLayoutView import Stacked_Layout_View

import os

class MainView(QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        
        self.setWindowTitle ('Searcher')
        self.setWindowIcon (QtGui.QIcon ("./Image/favicon.png"))
        
        self.applyStyles ()
        
        self.main_layout = QGridLayout ()
        
        self.home_view       = HeaderView ()
        self.stacked_layout_view = Stacked_Layout_View ()

        self.main_layout.addWidget (self.home_view, 0, 0, 1, 12)
        self.main_layout.addWidget (self.stacked_layout_view, 1, 0, 11, 12)

        self.setLayout (self.main_layout)

        self.main_controller = MainController ()
        
    def applyStyles(self):
        primary_color = "rgba(44, 140, 142, 0.5)"
        secondary_color = "#C5C5C5"
        background_color = "#F5F5F5"    
        text_color = "#333333"
        button_color = "#2C8C8E"
        button_color_hover = "#2C6E8F"  ##2C6E8F
        button_color_pressed = "#2C8F6F"    ##2C8F6F
        button_text_color = "#FFFFFF"
        remove_button_color = "#E74C3C"

        # Apply palette for background and text color
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(background_color))
        palette.setColor(QPalette.WindowText, QColor(text_color))
        self.setPalette(palette)

        range_group_box = (f"""
                QGroupBox#Range_Group_Box {{
                border: none;
                background-color: #dddddd;
                padding: 10px;
                margin: 10px 0;
                border-radius: 5px;
            }}
            QLabel#setting_attribute {{
                font-size: 10px;
                color: gray;
                background-color: #dddddd;
            }}
            QLabel#setting_attribute_value{{
                color: black;
                background-color: #dddddd;
            }}
            """)
        
        range_group_box_2 = (f"""
                QGroupBox#Range_Group_Box {{
                border: none;
                background-color: {background_color};
                padding: 10px;
                margin: 10px 0;
                border-bottom: 2px solid {primary_color};
            }}
            QLabel#setting_attribute {{
                font-size: 10px;
                color: gray;
                background-color: {background_color};
            }}
            QLabel#setting_attribute_value{{
                color: black;
                background-color: {background_color};
            }}
            """)

        # Apply stylesheet
        self.setStyleSheet(f"""
            QDoubleSpinBox {{
                border: 1px solid {secondary_color};
                border-radius: 5px;
                padding: 5px;
                background-color: {background_color};
                color: {text_color};
            }}
            QWidget {{
                background-color: {background_color};
                color: {text_color};
            }}
            {range_group_box_2}
            QGroupBox {{
                border: none;
                background-color: {background_color};
                padding: 10px;
                margin: 10px 0;
            }}
            QLineEdit {{
                border: 1px solid {secondary_color};
                padding: 5px;
                border-radius: 5px;
            }}
            QPushButton {{
                background-color: {button_color};
                color: {button_text_color};
                border: none;
                padding: 10px;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                background-color: {button_color_hover};
                opacity: 0.8;
            }}
            QPushButton:pressed {{
                background-color: {button_color_pressed};
                opacity: 0.8;
            }}
            QPushButton#remove {{
                background-color: {button_color};
                color: {button_text_color};
                min-width: 150px;
                max-width: 150px;
            }}
            QPushButton#remove:hover {{
                opacity: 0.8;
                background-color: {button_color_hover};
            }}
            QPushButton#remove:pressed {{
                opacity: 0.8;
                background-color: {button_color_pressed};
            }}
            QComboBox {{
                border: 1px solid {secondary_color};
                border-radius: 5px;
                padding: 5px;
                background-color: {button_text_color};
                color: {text_color};
            }}
            QComboBox::drop-down:hover {{
                background-color: #E0E0E0;
            }}
            QComboBox::item {{
                padding: 5px;
            }}
            QComboBox::item:selected {{
                background-color: #2C8C8E;
                color: {button_text_color};
            }}
            QScrollArea {{
                border: none;
            }}
            
        """)
        