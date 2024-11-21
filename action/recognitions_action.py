import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR
        
class RecognitionsAction(QThread):
    progressUpdated = Signal(int)
    batchFinished = Signal()

    def __init__(self, engine, dataModelMap):
        super().__init__()
        self.engine = engine
        self.dataModelMap = dataModelMap

    def run(self):
        print("RecognitionsAction 开始识别")
        imageCount = len(self.dataModelMap)
        for index, dataModel in self.dataModelMap.items():
            imgPath = dataModel.targetImage
            result, elapse = self.engine(imgPath, use_det=True, use_cls=False, use_rec=True) # 检测+识别
            texts = [item[1] for item in result]
            target_text = '号码'
            for text in texts:
                if text.startswith(target_text):
                    # print(text) # 号码：01819689
                    numbers = ''.join(filter(str.isdigit, text))
                    # print(numbers)
                    dataModel.addStashResult(numbers)
 
            progress = (index + 1) * 100 // imageCount
            self.progressUpdated.emit(progress)
        self.batchFinished.emit()
        print("RecognitionsAction 识别完成")