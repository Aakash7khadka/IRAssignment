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
    cluster_documents = pyqtSignal (list)
    
    def __init__(self, controller: StackeLayoutController) -> None:
        super().__init__()

        self.search_controller = controller.search_controller
        self.stacked_layout_controller = controller
        
        self.main_grid_layout = QGridLayout ()
        
        self.input_line_edit = QLineEdit ()
        self.search_button = QPushButton ("Search")
        self.search_button.pressed.connect (self.search)
        self.change_to_cluster_view_button = QPushButton ("Cluster")
        self.change_to_cluster_view_button.pressed.connect (lambda: self.change_stacked_layout_change.emit ())
        self.search_controller.send_relevant_document_list.connect (self.display_relevant_documents)
        

        self.scroll_widget = QWidget ()
        self.scroll_layout = QVBoxLayout ()
        self.scroll_layout.setAlignment(Qt.AlignTop)
        self.scroll_widget.setLayout (self.scroll_layout)

        self.scroll_area = QScrollArea ()
        self.scroll_area.setWidgetResizable (True)
        self.scroll_area.setWidget (self.scroll_widget)

        self.rel_doc_1 = self.build_relevant_doc_for_display ("Your search results will be displayed here",
                                                              "")
       
        self.scroll_layout.addWidget (self.rel_doc_1)


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
        key_word_label.setObjectName ("header")
        description_label = QLabel (description)

        v_layout.addWidget (key_word_label)
        v_layout.addWidget (description_label)

        range_box.setLayout (v_layout)
        
        return range_box

    def search (self):
        query = self.input_line_edit.text()
        self.search_controller.search (query)

    def display_relevant_documents (self, doc_list):
        while self.scroll_layout.count() > 0:
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for doc in doc_list:
            rel_doc = self.build_relevant_doc_for_display (doc[0],doc[1])
        
            self.scroll_layout.addWidget (rel_doc)

        self.cluster_documents.emit (doc_list)
