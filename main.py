import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel
from PySide6.QtGui import QPixmap

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)

        # 左边布局
        leftLayout = QVBoxLayout()
        self.uploadButton = QPushButton("上传图片")
        self.imageList = QListWidget()
        leftLayout.addWidget(self.uploadButton)
        leftLayout.addWidget(self.imageList)

        # 右边布局
        rightLayout = QVBoxLayout()
        self.recognizeButton = QPushButton("识别")
        self.resultLabel = QLabel()
        rightLayout.addWidget(self.recognizeButton)
        rightLayout.addWidget(self.resultLabel)

        # 主布局
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)

        
    def recognizeImage(self):
        currentItem = self.imageList.currentItem()
        if currentItem:
            filePath = currentItem.text()
            image = Image.open(filePath)
            ocr = paddleocr.PaddleOCR(lang='ch')
            result = ocr.ocr(image, cls=True)
            self.resultLabel.setText(result[0][1][0])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())