import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

class RecognitionThread(QThread):
    progressUpdated = Signal(int)
    finished = Signal()

    def __init__(self, imageList, resultList):
        super().__init__()
        self.imageList = imageList
        self.resultList = resultList

    def run(self):
        imageListSize = self.imageList.count()
        for i in range(imageListSize):
            imgPath = self.imageList.item(i).text()
            result, elapse = engine(imgPath, use_det=True, use_cls=False, use_rec=True) # 检测+识别
            texts = [item[1] for item in result]
            target_text = '号码'
            for text in texts:
                if text.startswith(target_text):
                    # print(text) # 号码：01819689
                    numbers = ''.join(filter(str.isdigit, text))
                    print(numbers)
                    self.resultList.addItem(numbers)
                    
            progress = (i + 1) * 100 // imageListSize
            self.progressUpdated.emit(progress)
        self.finished.emit()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 800)

        # 左边布局
        leftLayout = QVBoxLayout()
        self.imageCountLabel = QLabel("图片数量: 0")
        leftLayout.addWidget(self.imageCountLabel)
        self.imageList = QListWidget()
        leftLayout.addWidget(self.imageList)

        # 中间布局
        centerLayout = QVBoxLayout()
        self.uploadButton = QPushButton("上传图片")
        centerLayout.addWidget(self.uploadButton)
        self.uploadButton.clicked.connect(self.uploadImage)
        
        self.recognizeButton = QPushButton("识别")
        centerLayout.addWidget(self.recognizeButton)
        self.recognizeButton.clicked.connect(self.recognizeImage)
        
        self.sbDiffValue = QSpinBox()
        self.sbDiffValue.setRange(1, 5000)
        self.sbDiffValue.setValue(100)
        centerLayout.addWidget(self.sbDiffValue)
        
        self.btnCheckResult = QPushButton("校验")
        centerLayout.addWidget(self.btnCheckResult)
        self.btnCheckResult.clicked.connect(self.checkResult)
        
        self.btnClean = QPushButton("清除")
        centerLayout.addWidget(self.btnClean)
        self.btnClean.clicked.connect(self.cleanAll)

        # 右边布局
        rightLayout = QVBoxLayout()
        self.resultCountLabel = QLabel("识别数量: 0")
        rightLayout.addWidget(self.resultCountLabel)
        self.resultList = QListWidget()
        rightLayout.addWidget(self.resultList)

        # 主布局
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(centerLayout)
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)


    def uploadImage(self):
        filePaths, _ = QFileDialog.getOpenFileNames(self, "选择图片", "", "图片文件 (*.jpg *.png *.bmp)")
        if filePaths:
            for filePath in filePaths:
                self.imageList.addItem(filePath)
            self.imageCountLabel.setText(f"图片数量: {self.imageList.count()}")
            

    def recognizeImage(self):
        self.loading_dialog = QProgressDialog("正在识别...", "取消", 0, 100, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.show()
        
        self.recognitionThread = RecognitionThread(self.imageList, self.resultList)
        self.recognitionThread.progressUpdated.connect(self.updateProgressDialog)
        self.recognitionThread.finished.connect(self.recognitionFinished)
        self.recognitionThread.start()
        
        
    def checkResult(self):
        diffValue = self.sbDiffValue.value()
        if diffValue<=0:
            QMessageBox.warning(self, "异常", "请设定合理的临界值")
            return
        
        for i in range(self.resultList.count() - 1):
            item1 = self.resultList.item(i).text()
            item2 = self.resultList.item(i + 1).text()
            
            # 这里假设item1和item2都是数字，你可以根据实际情况修改
            if item1.isdigit() and item2.isdigit():
                diff = abs(int(item1) - int(item2))
                if diff < 100:
                    QMessageBox.warning(self, "错误", f"发现相邻号码差值小于100, 号码: {item1} 和 {item2}")
                    return
            else:
                QMessageBox.warning(self, f"识别结果不是数字: {item1} 或 {item2}")
        
        QMessageBox.information(self, "校验通过", "未发现异常号码")
        
        
    def updateProgressDialog(self, progress):
        self.loading_dialog.setValue(progress)
        
        
    def recognitionFinished(self):
        self.loading_dialog.close()
        self.resultCountLabel.setText(f"识别数量: {self.resultList.count()}")
        self.resultList.sortItems()
        
        
    def cleanAll(self):
        self.imageList.clear()
        self.resultList.clear()
        self.imageCountLabel.setText(f"图片数量: {self.imageList.count()}")
        self.resultCountLabel.setText(f"识别数量: {self.resultList.count()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())