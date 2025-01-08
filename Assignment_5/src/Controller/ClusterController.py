from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)

import threading
import time

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

class ClusterController (QObject):
    
    change_stacked_layout_change = pyqtSignal (str)
    cluster_data = pyqtSignal (np.ndarray, list, np.ndarray)

    def __init__(self):
        super().__init__()

    def cluster (self, doc_list):

        one_dim_doc_list = [doc[0] + ". " + doc[1] for doc in doc_list]

        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(one_dim_doc_list)

        num_clusters = 3  
        kmeans = KMeans(n_clusters=num_clusters, random_state=42)
        kmeans.fit(X)

        cluster_labels = kmeans.labels_

        pca = PCA(n_components=2)
        reduced_data = pca.fit_transform(X.toarray())   

        self.cluster_data.emit (reduced_data, one_dim_doc_list, cluster_labels)
        