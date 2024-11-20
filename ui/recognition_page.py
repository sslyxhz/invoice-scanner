from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from model.data_model import DataModel
from action.recognition_action import RecognitionAction

class RecognitionPage(QWidget):
    
    signal_image_selected = Signal(int)
    
    def __init__(self, dataModel):
        super().__init__()
        self.dataModel = dataModel
        self.initUI()
    
    def initUI(self):
        pageLayout = QHBoxLayout()  # 创建水平布局
        self.setLayout(pageLayout) 
        
        # 左边布局
        leftLayout = QVBoxLayout()
        
        self.imagePreviewLabel = QLabel()
        leftLayout.addWidget(self.imagePreviewLabel)
        pixmap = QPixmap(self.dataModel.targetImage)
        self.imagePreviewLabel.setPixmap(pixmap)
        

        # 中间布局
        centerLayout = QVBoxLayout()
        
        # 识别按钮
        self.recognizeButton = QPushButton("识别")
        self.recognizeButton.clicked.connect(self.recognizeImage)
        centerLayout.addWidget(self.recognizeButton)
        
        # 阈值设定
        self.sbDiffValue = QSpinBox()
        self.sbDiffValue.setRange(1, 5000)
        self.sbDiffValue.setValue(100)
        centerLayout.addWidget(self.sbDiffValue)
        
        # 准备校验按钮
        self.btnOk = QPushButton("确认结果")
        self.btnOk.clicked.connect(self.checkResult)
        centerLayout.addWidget(self.btnCheckResult)

        # 右边布局
        rightLayout = QVBoxLayout()
        
        self.tmpResultList = QListWidget()
        rightLayout.addWidget(self.tmpResultList)

        # 主布局
        pageLayout.addLayout(leftLayout)
        pageLayout.addLayout(centerLayout)
        pageLayout.addLayout(rightLayout)

    # 识别图片
    def recognizeImage(self):
        self.loading_dialog = QProgressDialog("正在识别...", "取消", 0, 100, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.show()
        
        self.recognitionThread = RecognitionAction(self.dataModel.targetImage, self.tmpResultList)
        self.recognitionThread.progressUpdated.connect(self.updateProgressDialog)
        self.recognitionThread.finished.connect(self.recognitionFinished)
        self.recognitionThread.start()
        

