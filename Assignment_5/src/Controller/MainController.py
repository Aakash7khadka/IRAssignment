
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QVBoxLayout
)

from PyQt5 import(
    QtGui
)

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)


import os

class MainController(QWidget):
    
    load_settings = pyqtSignal (str)
    
    def __init__(self) -> None:
        super().__init__()
        
        
        
        
        