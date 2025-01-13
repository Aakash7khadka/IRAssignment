import numpy as np
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class MatplotlibWidget(QWidget):


    def __init__(self, parent=None) -> None:
        
        # in order to embed the graph the class inherits QWidget and hence, needs to call super constructor
        super(MatplotlibWidget, self).__init__(parent)
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
                
        '''
        create a layout and place the graph under the menuebar
        '''
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.toolbar)
        self.layout().addWidget(self.canvas)
        self.ax = self.figure.add_subplot(111)
        
        self.ax.set_title ("Clustered Search Results")
        self.figure.tight_layout()

        self.x = []
        self.y = []
        self.labels = []
    
        
    def set_suptitle (self, str: str, color: str) -> None:
        self.figure.suptitle (str, weight='bold', x=.3, y=.2,
                        backgroundcolor=color)
        
        self.canvas.draw ()
        
    def save_plot (self, name: str) -> None:
        self.ax.grid (True)
        self.ax.scatter (self.x, self.y)
        self.figure.savefig (name, dpi = 600)
        
    def _display_plot (self):
        self.ax.grid (True)
        scatter = self.ax.scatter (self.x, self.y, c=self.labels, cmap='viridis', s=100)
        colorbar = self.figure.colorbar(scatter, ax=self.ax, orientation='vertical')
        colorbar.set_label('')
                            
    def plot(self) -> None:
        self.ax.clear()
        self._display_plot ()
        self.canvas.draw()

    def set_x_y_label (self, x, y, labels):
        self.x = x
        self.y = y
        self.labels = labels

    def set_title (self, title: str) -> None:
        self.ax.set_title(title)

    def annotate (self, annotations):
        for i, txt in enumerate(annotations):
            self.ax.annotate(
                txt[:50],  
                (self.x[i], self.y[i]),
                fontsize=8
            )

    def clear_plot(self) -> None:
        self.ax.clear()  
        self.ax.set_title("Clustered Search Results")  
        
