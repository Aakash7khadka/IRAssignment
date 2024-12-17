from PyQt5.QtWidgets import (
    QWidget,
    QStackedLayout,
    QHBoxLayout
)

from src.View.SearchView import SearchView
from src.View.ClusterView import ClusterView


class Stacked_Layout_View (QWidget):

    def __init__ (self): 
        super ().__init__ ()

        self.initStackedLayoutView ()

    def initStackedLayoutView (self):

        self.stackedLayout          = QStackedLayout ()

        self.search_view             = SearchView ()

        self.cluster_view           = ClusterView ()

        self.stackedLayout.addWidget (self.search_view)
        self.stackedLayout.addWidget (self.cluster_view)     
        
        self.setLayout (self.stackedLayout)