import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("图片识别")
        self.setGeometry(100, 100, 1000, 800)
        self.current_page = 1
        self.pages = [
            self.page1(),
            self.page2(),
            # ... add more pages
        ]
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.pages[0])

    def page1(self):
        # ... create UI for page 1
        next_button = QPushButton("下一步")
        next_button.clicked.connect(self.nextPage)
        # ... add other widgets to page 1
        return QWidget()

    def page2(self):
        # ... create UI for page 2
        back_button = QPushButton("返回")
        back_button.clicked.connect(self.prevPage)
        next_button = QPushButton("下一步")
        next_button.clicked.connect(self.nextPage)
        # ... add other widgets to page 2
        return QWidget()

    def nextPage(self):
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.layout().removeWidget(self.pages[self.current_page - 1])
        self.layout().addWidget(self.pages[self.current_page])
        self.layout().update()

    def prevPage(self):
        self.current_page = (self.current_page - 1) % len(self.pages)
        self.layout().removeWidget(self.pages[self.current_page + 1])
        self.layout().addWidget(self.pages[self.current_page])
        self.layout().update()
        
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())