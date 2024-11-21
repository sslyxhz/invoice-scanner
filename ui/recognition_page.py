from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox, QInputDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from model.data_model import DataModel
from action.recognition_action import RecognitionAction

class RecognitionPage(QWidget):
    
    signal_result_checked = Signal(str)
    
    def __init__(self, engine, dataModel):
        super().__init__()
        self.engine = engine
        self.dataModel = dataModel
        self.initUI()

        # 加载完成后就直接进入识别
        self.recognizeImage()
    
    def initUI(self):
        pageLayout = QHBoxLayout()  # 创建水平布局
        self.setLayout(pageLayout) 
        
        # 左边布局
        leftLayout = QVBoxLayout()
        
        self.imagePreviewLabel = QLabel()
        leftLayout.addWidget(self.imagePreviewLabel)
        pixmap = QPixmap(self.dataModel.targetImage)
        scaled_pixmap = pixmap.scaled(400, 300)
        self.imagePreviewLabel.setPixmap(scaled_pixmap)
        

        # 中间布局
        centerLayout = QVBoxLayout()
        
        # 识别按钮
        self.recognizeButton = QPushButton("再次识别")
        self.recognizeButton.clicked.connect(self.recognizeImage)
        centerLayout.addWidget(self.recognizeButton)
        
        # 阈值设定
        self.sbDiffValue = QSpinBox()
        self.sbDiffValue.setRange(1, 5000)
        self.sbDiffValue.setValue(100)
        centerLayout.addWidget(self.sbDiffValue)
        
        # 准备校验按钮
        self.btnOk = QPushButton("确认识别结果")
        self.btnOk.clicked.connect(self.checkRecogResult)
        centerLayout.addWidget(self.btnOk)

        # 右边布局
        rightLayout = QVBoxLayout()

        # 右边布局 - 统计
        self.resultCountLabel = QLabel("识别结果数: 0")
        rightLayout.addWidget(self.resultCountLabel)

        # 右边布局 - 操作
        self.operateBox = QHBoxLayout()
        self.btnAdd = QPushButton("添加")
        self.btnAdd.clicked.connect(self.addStashResult)
        self.operateBox.addWidget(self.btnAdd)

        self.btnEdit = QPushButton("编辑")
        self.btnEdit.clicked.connect(self.editdStashResult)
        self.operateBox.addWidget(self.btnEdit)

        self.btnDel = QPushButton("删除")
        self.btnDel.clicked.connect(self.delStashResult)
        self.operateBox.addWidget(self.btnDel)

        rightLayout.addLayout(self.operateBox)
        
        # 右边布局 - 列表
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
        
        self.recognitionThread = RecognitionAction(self.engine, self.dataModel)
        # self.recognitionThread.progressUpdated.connect(self.updateProgressDialog)
        self.recognitionThread.finished.connect(self.recognitionFinished)
        self.recognitionThread.start()
    
    def updateProgressDialog(self, progress):
        self.loading_dialog.setValue(progress)

    def recognitionFinished(self):
        self.loading_dialog.close()
        self.tmpResultList.clear()
        self.tmpResultList.addItems(self.dataModel.stashResultList)
        self.resultCountLabel.setText(f"识别结果数: {self.dataModel.stashResultList.count()}")

    def addStashResult(self):
        text, ok = QInputDialog.getText(self, '添加结果', '请输入新的识别结果:')
        if ok and text:
            self.dataModel.addStashResult(text)
            self.tmpResultList.addItem(text)
            self.updateResultCountLabel()

    def editdStashResult(self):
        currentItem = self.tmpResultList.currentItem()
        if currentItem is None:
            QMessageBox.warning(self, "提示", "请先选择要编辑的项")
            return
            
        text = currentItem.text()
        row = self.tmpResultList.row(currentItem)
        new_text, ok = QInputDialog.getText(self, '编辑结果', '请输入新的识别结果:', text=text)
        if ok and new_text:
            self.dataModel.editStashResult(text, new_text)
            self.tmpResultList.takeItem(row)
            self.tmpResultList.insertItem(row, new_text)
            self.updateResultCountLabel()

    def delStashResult(self):
        currentItem = self.tmpResultList.currentItem()
        if currentItem is None:
            QMessageBox.warning(self, "提示", "请先选择要删除的项")
            return
            
        text = currentItem.text()
        row = self.tmpResultList.row(currentItem)
        self.tmpResultList.takeItem(row)
        self.dataModel.removeStashResult(text)
        self.updateResultCountLabel()

    def updateResultCountLabel(self):
        self.resultCountLabel.setText(f"识别结果数: {len(self.dataModel.stashResultList)}")

    # 确认识别结果
    def checkRecogResult(self):
        self.signal_result_checked.emit(self.dataModel.index)

