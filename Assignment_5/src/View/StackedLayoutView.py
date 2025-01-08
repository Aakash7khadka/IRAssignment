from PyQt5.QtWidgets import (
    QWidget,
    QStackedLayout,
    QHBoxLayout
)

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src.View.SearchView import SearchView
from src.View.ClusterView import ClusterView
from src.Controller.StackedLayoutController import StackeLayoutController
from src.Controller.SearchController import SearchController
from src.Controller.ClusterController import ClusterController

class Stacked_Layout_View (QWidget):



    def __init__ (self): 
        super ().__init__ ()

        self.initStackedLayoutView ()
        self.process_signals ()

    def initStackedLayoutView (self):

        self.stacked_layout_controller = StackeLayoutController ()
        

        self.stackedLayout          = QStackedLayout ()

        self.search_view             = SearchView (self.stacked_layout_controller)

        self.cluster_view           = ClusterView (self.stacked_layout_controller)

        self.stackedLayout.addWidget (self.search_view)
        self.stackedLayout.addWidget (self.cluster_view)     
        
        self.setLayout (self.stackedLayout)

    def process_signals (self):
        self.search_view.change_stacked_layout_change.connect (self.display_cluster_view)
        self.cluster_view.change_stacked_layout_change.connect (self.display_search_view)
        self.search_view.cluster_documents.connect (self.cluster)

    def display_cluster_view (self):
        self.stackedLayout.setCurrentIndex (1)

    def display_search_view (self):
        self.stackedLayout.setCurrentIndex (0)

    def cluster (self, doc_list: list):
        self.stacked_layout_controller.cluster_controller.cluster (doc_list)