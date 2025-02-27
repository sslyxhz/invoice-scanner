from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from model.data_model import DataModel

class IndexPage(QWidget):
    
    signal_image_selected = Signal(int)
    
    def __init__(self, dataModelMap):
        super().__init__()
        self.initUI()
        self.dataModelMap = dataModelMap
    
    def initUI(self):
        layout = QHBoxLayout()
        self.setLayout(layout) 
        
        btnUpload = QPushButton("选择图片")
        btnUpload.clicked.connect(self.select_image)
        layout.addWidget(btnUpload)  # 将按钮添加到布局中

    def select_image(self):
        filePaths, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "图片文件 (*.jpg *.png *.bmp *.heic)")
        if filePaths:
            for index, filePath in enumerate(filePaths):
                self.dataModelMap[index] = DataModel(index, filePath)
            self.signal_image_selected.emit(1)
        else:
            self.signal_image_selected.emit(0)
        

