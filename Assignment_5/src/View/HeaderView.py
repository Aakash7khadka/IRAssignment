from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout
)

from PyQt5.QtGui import(
    QFont,
    QPixmap
)
from PyQt5.QtCore import Qt


class HeaderView (QWidget):
    
    def __init__(self) -> None:
        super().__init__()
        
        home_layout = QHBoxLayout ()

        self.data_loaded_state_label = QLabel ("Search Engine By Group4[Gowtham Premkumar, Aakash Khadka, Max Neubauer]")
        #self.load_data_button = QPushButton ("Load Data")
        
        home_layout.addWidget (self.data_loaded_state_label)
        home_layout.addStretch ()
        #home_layout.addWidget (self.load_data_button)
        
        self.setLayout (home_layout)