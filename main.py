import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap, QFont, QBrush, QPalette
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

        # 使用 QPalette 设置背景
        palette = self.palette()
        pixmap = QPixmap('./assets/background.jpg')
        pixmap = pixmap.scaled(
            self.size(),
            Qt.KeepAspectRatioByExpanding,  # 保持比例填充
            Qt.SmoothTransformation  # 平滑处理
        )
        palette.setBrush(QPalette.Window, QBrush(pixmap))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        
        # 按钮等控件的样式
        self.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 255, 255, 0.9);
                border: 1px solid #ccc;
                padding: 5px;
            }
        """)
        
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
        print('跳转下一页 - 开始 cur page index: ', self.current_page_index)
        self.pages[self.current_page_index].hide()
        self.layout().removeWidget(self.pages[self.current_page_index])
        
        self.current_page_index = self.current_page_index + 1

        self.layout().addWidget(self.pages[self.current_page_index])
        self.pages[self.current_page_index].show()
        self.layout().update()
        print('跳转下一页 - 完成 cur page index: ', self.current_page_index)

        if isinstance(self.pages[self.current_page_index], ResultPage):
            self.pages[self.current_page_index].loadData()

    def prevPage(self):
        print('跳转上一页 - 开始, cur page index: ', self.current_page_index)
        
        self.pages[self.current_page_index].hide()
        self.layout().removeWidget(self.pages[self.current_page_index])
        
        self.current_page_index = self.current_page_index - 1

        self.layout().addWidget(self.pages[self.current_page_index])
        self.pages[self.current_page_index].show()
        self.layout().update()
        print('跳转上一页 - 完成, cur page index: ', self.current_page_index)
        

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
            recognition_page.signal_pre_step.connect(self.prevPage)
            # Add to pages list
            self.pages.append(recognition_page)
        resultPage = ResultPage(self.dataModelMap)
        resultPage.signal_check_result_done.connect(self.newRound)
        resultPage.signal_pre_step.connect(self.prevPage)
        self.pages.append(resultPage)

        # 记载数据
        for page in self.pages:
            if isinstance(page, RecognitionPage):
                page.loadData()

        # 跳转下一页
        self.nextPage()

    # 新一轮检测
    def newRound(self):
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

global_font = QFont()
global_font.setPointSize(18)  # 设置全局字体大小
global_font.setBold(True)      # 设置全局字体加粗

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setFont(global_font)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())