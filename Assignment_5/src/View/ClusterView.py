from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QTabWidget,
    QPushButton,
    QVBoxLayout,
    QGridLayout,
    QTextEdit,
    QGroupBox,
    QScrollArea,
    QLineEdit,
    QFormLayout,
    QRadioButton,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QComboBox
)

from PyQt5 import(
    QtGui
)
from PyQt5.QtGui import (
    QFont, 
    QIntValidator,
    QPixmap
)

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src.Utils.QtMatplotGraph import MatplotlibWidget

class ClusterView (QWidget):
    
   
    def __init__(self) -> None:
        super().__init__()
        
        self.main_grid_layout = QGridLayout ()
        
        self.input_line_edit = QLineEdit ()
        self.search_button = QPushButton ("Search")
        self.change_to_cluster_view_button = QPushButton ("Cluster")

        self.cluster_graph = MatplotlibWidget ()

        self.cluster_graph.set_x_y([1, 1.1, 1.3, 4, 4.2, 4.1], [1, 0.9, 1.1, 4, 3.9, 4.1])
        self.cluster_graph._display_plot ()
        
        self.main_grid_layout.addWidget (self.input_line_edit, 0, 0, 1, 10)
        self.main_grid_layout.addWidget (self.search_button, 0, 10, 1, 2)
        self.main_grid_layout.addWidget (self.cluster_graph, 1, 0, 10, 12)
        self.main_grid_layout.addWidget (self.change_to_cluster_view_button, 12, 4, 1, 4)

        self.setLayout (self.main_grid_layout)



        