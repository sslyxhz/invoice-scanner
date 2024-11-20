import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR
from ui.index_page import IndexPage
from ui.recognition_page import RecognitionPage
from model.data_model import DataModel

engine = RapidOCR()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.dataModelMap = {}
        
        self.setWindowTitle("图片识别")
        self.setGeometry(100, 100, 1000, 800)
        
        # 首页, 引导
        self.index_page = IndexPage(self.dataModelMap)
        self.index_page.signal_image_selected.connect(self.on_image_selected)
        
        self.current_page = 1
        self.pages = [
            self.index_page,
        ]
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.pages[0])


    def on_image_selected(self, value):
        if(value > 0):
            print("选择完成")
            for dataModel in self.dataModelMap.values():
                # Create recognition page
                recognition_page = RecognitionPage(dataModel)
                recognition_page.signal_result_checked.connect(self.on_recognition_ok)
                # Add to pages list
                self.pages.append(recognition_page)
            self.nextPage()
        else:
            print("选择失败")
    
    def on_recognition_ok(self, imagePath):
        if(imagePath):
            print('确认识别完成')

    def nextPage(self):
        print('开始跳转下一页')
        self.current_page = (self.current_page + 1) % len(self.pages)
        self.layout().removeWidget(self.pages[self.current_page - 1])
        self.layout().addWidget(self.pages[self.current_page])
        self.layout().update()
        print('跳转下一页完成')

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