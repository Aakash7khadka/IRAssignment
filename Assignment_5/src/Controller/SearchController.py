from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

import threading
import time

class SearchController (QObject):
    
    change_stacked_layout_change = pyqtSignal (str)

    def __init__(self):
        super().__init__()

    def search (self):
        '''
        Here goes the code for searching
        '''
        print ("Searching")
        