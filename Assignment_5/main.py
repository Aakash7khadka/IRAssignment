import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt, QPoint
import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from Assignment_5.create_index import get_reponse

class ClusteringVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Result Clustering Visualization")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Search input
        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Enter your search query")
        self.layout.addWidget(self.search_input)

        # Search button
        self.search_button = QPushButton("Search and Cluster", self)
        self.search_button.clicked.connect(self.cluster_results)
        self.layout.addWidget(self.search_button)

        # Visualization area
        self.canvas = QLabel(self)
        self.canvas.setMinimumSize(780, 500)
        self.canvas.setStyleSheet("background-color: white;")
        self.layout.addWidget(self.canvas)

    def cluster_results(self):
        query = self.search_input.text()
        results = get_reponse(query)
        mock_results = [x[1] for x in results]

        # Vectorize the text data
        vectorizer = TfidfVectorizer(stop_words='english')
        X = vectorizer.fit_transform(mock_results)

        # Perform K-means clustering
        kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
        labels = kmeans.labels_
        centers = kmeans.cluster_centers_

        # Draw clusters on the canvas
        self.draw_clusters(mock_results, labels)

    def draw_clusters(self, results, labels):
        if self.canvas.pixmap() is None:
            self.canvas.setPixmap(QPixmap(self.canvas.size()))
            self.canvas.pixmap().fill(Qt.white)
        painter = QPainter(self.canvas.pixmap())
        painter.begin(self.canvas.pixmap())

        # Clear previous drawings
        painter.fillRect(self.canvas.rect(), Qt.white)

        # Define colors for clusters
        colors = [QColor(255, 0, 0), QColor(0, 255, 0), QColor(0, 0, 255)]  # Red, Green, Blue

        # Randomly position points for visualization
        points = self.get_random_points(len(results))
        
        for i, (point, label) in enumerate(zip(points, labels)):
            painter.setPen(QPen(colors[label], 2))
            painter.drawEllipse(point, 5, 5)
            painter.drawText(point.x() + 10, point.y() + 5, results[i][:30] + '...')  # Only show first 30 chars

        painter.end()
        self.canvas.update()

    def get_random_points(self, n):
        width, height = self.canvas.width(), self.canvas.height()
        return [QPoint(np.random.randint(50, width - 50), np.random.randint(50, height - 50)) for _ in range(n)]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    visualizer = ClusteringVisualizer()
    visualizer.show()
    sys.exit(app.exec_())