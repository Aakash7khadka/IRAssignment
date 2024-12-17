import sys
from PyQt5.QtWidgets import (
    QApplication
)

from src.View.MainView import MainView

if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = MainView ()
    view.showMaximized ()
    sys.exit(app.exec_())