from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

import threading
import time

from src.Controller.SearchController import SearchController
from src.Controller.ClusterController import ClusterController

class StackeLayoutController (QObject):
    
    change_stacked_layout_change = pyqtSignal ()

    def __init__(self):
        super().__init__()

        self.search_controller = SearchController ()
        self.cluster_controller = ClusterController ()