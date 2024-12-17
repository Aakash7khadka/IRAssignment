from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

import threading
import time

class StackeLayoutController (QObject):
    
    change_stacked_layout_change = pyqtSignal (str)