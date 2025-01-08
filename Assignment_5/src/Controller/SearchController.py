from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

from src.Service.CustomElasticSearch import CustomElasticSearch

import threading
import time

class SearchController (QObject):
    
    change_stacked_layout_change = pyqtSignal (str)
    send_relevant_document_list = pyqtSignal (list)

    def __init__(self):
        super().__init__()
        self.elasticSearchService = CustomElasticSearch()


    def search (self, query: str):
        
        response = self.elasticSearchService.get_reponse (query=query)
        self.send_relevant_document_list.emit (response)
        