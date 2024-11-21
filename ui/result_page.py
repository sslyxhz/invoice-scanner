from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from model.data_model import DataModel

class ResultPage(QWidget):
    
    signal_image_selected = Signal(int)
    
    def __init__(self, dataModelMap):
        super().__init__()
        self.initUI()
        self.dataModelMap = dataModelMap
    
    def initUI(self):
        layout = QHBoxLayout()  # 创建水平布局
        self.setLayout(layout) 
        
        btnUpload = QPushButton("选择图片222")
        # btnUpload.clicked.connect(self.select_image)
        layout.addWidget(btnUpload)  # 将按钮添加到布局中

        

