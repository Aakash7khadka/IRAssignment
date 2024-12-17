from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QFormLayout,
    QVBoxLayout,
    QPushButton,
    QGridLayout,
    QGroupBox,
    QTextEdit,
    QComboBox,
    QDoubleSpinBox,
    QAbstractSpinBox,
    QRadioButton,
    QLineEdit,
    QHBoxLayout,
    QScrollArea,
    QLabel
)

from PyQt5 import(
    QtGui
)

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src.Controller.SearchController import SearchController
from src.Controller.StackedLayoutController import StackeLayoutController

class SearchView (QWidget):
    
    change_stacked_layout_change = pyqtSignal ()
    
    def __init__(self, controller: StackeLayoutController) -> None:
        super().__init__()

        self.search_controller = controller.search_controller
        self.stacked_layout_controller = controller
        
        self.main_grid_layout = QGridLayout ()
        
        self.input_line_edit = QLineEdit ()
        self.search_button = QPushButton ("Search")
        self.search_button.pressed.connect (lambda: self.search_controller.search ())
        self.change_to_cluster_view_button = QPushButton ("Cluster")
        self.change_to_cluster_view_button.pressed.connect (lambda: self.change_stacked_layout_change.emit ())
        

        self.scroll_widget = QWidget ()
        self.scroll_layout = QVBoxLayout ()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_widget.setLayout (self.scroll_layout)

        self.scroll_area = QScrollArea ()
        self.scroll_area.setWidgetResizable (True)
        self.scroll_area.setWidget (self.scroll_widget)

        self.rel_doc_1 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        self.rel_doc_2 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        self.rel_doc_3 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        self.rel_doc_4 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        self.rel_doc_5 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        self.rel_doc_6 = self.build_relevant_doc_for_display ("Machine Learning",
                                                              "This is a test description to get the basic idea of how this is going to look in the UI.")
        
        self.scroll_layout.addWidget (self.rel_doc_1)
        self.scroll_layout.addWidget (self.rel_doc_2)
        self.scroll_layout.addWidget (self.rel_doc_3)
        self.scroll_layout.addWidget (self.rel_doc_4)
        self.scroll_layout.addWidget (self.rel_doc_5)
        self.scroll_layout.addWidget (self.rel_doc_6)


        self.main_grid_layout.addWidget (self.input_line_edit, 0, 0, 1, 10)
        self.main_grid_layout.addWidget (self.search_button, 0, 10, 1, 2)
        self.main_grid_layout.addWidget (self.scroll_area, 1, 0, 10, 12)
        self.main_grid_layout.addWidget (self.change_to_cluster_view_button, 12, 4, 1, 4)

        self.setLayout (self.main_grid_layout)
        
    def build_relevant_doc_for_display (self, key_word, description):
        range_box = QGroupBox("")
        range_box.setObjectName ("Range_Group_Box")
        
        v_layout = QVBoxLayout ()

        key_word_label = QLabel (key_word)
        description_label = QLabel (description)

        v_layout.addWidget (key_word_label)
        v_layout.addWidget (description_label)

        range_box.setLayout (v_layout)
        
        return range_box


