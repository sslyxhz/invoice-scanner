import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog
from PySide6.QtGui import QPixmap
from rapidocr_onnxruntime import RapidOCR

engine = RapidOCR()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1000, 800)

        # 左边布局
        leftLayout = QVBoxLayout()
        self.uploadButton = QPushButton("上传图片")
        self.imageList = QListWidget()
        leftLayout.addWidget(self.uploadButton)
        leftLayout.addWidget(self.imageList)
        self.uploadButton.clicked.connect(self.uploadImage)

        # 中间布局
        centerLayout = QVBoxLayout()
        self.recognizeButton = QPushButton("识别")
        centerLayout.addWidget(self.recognizeButton)
        self.recognizeButton.clicked.connect(self.recognizeImage)
        self.btnClean = QPushButton("清除")
        centerLayout.addWidget(self.btnClean)
        self.btnClean.clicked.connect(self.cleanAll)

        # 右边布局
        rightLayout = QVBoxLayout()
        self.resultList = QListWidget()
        rightLayout.addWidget(self.resultList)

        # 主布局
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(centerLayout)
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)


    def uploadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.jpg *.png *.bmp)")
        if filePath:
            self.imageList.addItem(filePath)
            

    def recognizeImage(self):
        for i in range(self.imageList.count()):
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
        # img_path = 'test.jpg'
        # result, elapse = engine(img_path, use_det=True, use_cls=False, use_rec=True) # 检测+识别
        # texts = [item[1] for item in result]
        # target_text = '号码'
        # for text in texts:
        #     if text.startswith(target_text):
        #         # print(text) # 号码：01819689
        #         numbers = ''.join(filter(str.isdigit, text))
        #         print(numbers)
        #         self.resultList.addItem(numbers)

    def cleanAll(self):
        self.imageList.clear()
        self.resultList.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())