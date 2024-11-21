import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR
        
class RecognitionAction(QThread):
    progressUpdated = Signal(int)
    finished = Signal()
    
    def __init__(self, engine, dataModel):
        super().__init__()
        self.engine = engine
        self.dataModel = dataModel
        
    def run(self):
        imgPath = self.dataModel.targetImage
        result, elapse = self.engine(imgPath, use_det=True, use_cls=False, use_rec=True) # 检测+识别
        texts = [item[1] for item in result]
        target_text = '号码'
        for text in texts:
            if text.startswith(target_text):
                # print(text) # 号码：01819689
                numbers = ''.join(filter(str.isdigit, text))
                print(numbers)
                self.dataModel.addStashResult(numbers)
            # self.progressUpdated.emit(progress)
        self.finished.emit()