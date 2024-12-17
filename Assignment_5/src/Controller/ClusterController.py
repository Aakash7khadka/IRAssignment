from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

import threading
import time

class ClusterController (QObject):
    
    change_stacked_layout_change = pyqtSignal (str)

    def __init__(self):
        super().__init__()

    def cluster (self):
        '''
        Here goes the code for clustering
        '''
        print ("Clustering")
        