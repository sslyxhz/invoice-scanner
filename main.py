import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR
from model.data_model import DataModel
from action.recognitions_action import RecognitionsAction
from ui.index_page import IndexPage
from ui.recognition_page import RecognitionPage
from ui.result_page import ResultPage

engine = RapidOCR()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("图片识别")
        self.setGeometry(100, 100, 1000, 800)
        self.current_page_index = 0
        
        self.newRound()


    def on_image_selected(self, value):
        if(value > 0):
            print("选择完成")

            # 直接执行识别任务
            self.recognizeImage()
        else:
            print("选择失败")
    
    def on_recognition_ok(self, modelIndex):
        print(f"确认识别完成 image: {modelIndex}")
        self.nextPage()

    def nextPage(self):
        print('开始跳转下一页')
        # self.current_page_index = (self.current_page_index + 1) % len(self.pages)
        self.current_page_index = self.current_page_index + 1
        self.pages[self.current_page_index - 1].hide()
        self.layout().removeWidget(self.pages[self.current_page_index - 1])
        self.layout().addWidget(self.pages[self.current_page_index])
        self.layout().update()
        print('跳转下一页完成 cur page index: ', self.current_page_index)

    def prevPage(self):
        print('开始跳转上一页')
        # self.current_page_index = (self.current_page_index - 1) % len(self.pages)
        self.current_page_index = self.current_page_index - 1
        self.pages[self.current_page_index + 1].hide()
        self.layout().removeWidget(self.pages[self.current_page_index + 1])
        self.layout().addWidget(self.pages[self.current_page_index])
        self.layout().update()
        print('跳转上一页完成 cur page index: ', self.current_page_index)
        

    # 识别图片
    def recognizeImage(self):
        self.loading_dialog = QProgressDialog("正在识别...", "取消", 0, 100, self)
        self.loading_dialog.setWindowModality(Qt.WindowModal)
        self.loading_dialog.show()
        
        self.recognitionThread = RecognitionsAction(engine, self.dataModelMap)
        self.recognitionThread.progressUpdated.connect(self.updateProgressDialog)
        self.recognitionThread.batchFinished.connect(self.recognitionFinished)
        self.recognitionThread.start()

    def updateProgressDialog(self, progress):
        print("更新进度", progress)
        self.loading_dialog.setValue(progress)

    def recognitionFinished(self):
        print("完成批量识别")
        self.loading_dialog.close()

        print("加载页面")
        for dataModel in self.dataModelMap.values():
            # Create recognition page
            recognition_page = RecognitionPage(engine, dataModel)
            recognition_page.signal_result_checked.connect(self.on_recognition_ok)
            # Add to pages list
            self.pages.append(recognition_page)
        resultPage = ResultPage(self.dataModelMap)
        resultPage.signal_check_result_done.connect(self.newRound)
        self.pages.append(resultPage)

        # 记载数据
        for page in self.pages:
            if isinstance(page, RecognitionPage):
                page.loadData()

        # 跳转下一页
        self.nextPage()

    # 新一轮检测
    def newRound(self):
        print("newRound...")

        if self.current_page_index > 0:
            self.pages[self.current_page_index].hide()
            self.layout().removeWidget(self.pages[self.current_page_index])
        
        self.dataModelMap = {}
        
        # 首页, 引导
        self.index_page = IndexPage(self.dataModelMap)
        self.index_page.signal_image_selected.connect(self.on_image_selected)
        
        # 加载首页
        self.current_page_index = 0
        self.pages = [
            self.index_page,
        ]
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.pages[0])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())