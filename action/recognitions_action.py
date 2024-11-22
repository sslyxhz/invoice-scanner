import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QFileDialog, QProgressDialog, QMessageBox, QSpinBox
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QThread, Signal
from rapidocr_onnxruntime import RapidOCR
from PIL import Image
        
# 按照位置排序
def get_text_position(item, image_height):
    box = item[0]  # 获取文本框坐标
    y = box[0][1]  # 左上角y坐标
    x = box[0][0]  # 左上角x坐标
    
    # y坐标在图片上1/3的分到第一组(group=0)，其余分到第二组(group=1)
    group = 0 if y <= image_height/3 else 1
    
    # 返回 (组号, x坐标) 作为排序依据
    return (group, x)


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

            # 使用前先获取图片高度
            img = Image.open(imgPath)
            img_height = img.height

            result, elapse = self.engine(imgPath, use_det=True, use_cls=False, use_rec=True) # 检测+识别

            sorted_result = sorted(result, key=lambda item: get_text_position(item, img_height))

            texts = [item[1] for item in sorted_result]
            for text in texts:
                if text.startswith('号码') or text.startswith('母码') or text.startswith('务码') or text.startswith('粤码'):
                    # print(text) # 号码：01819689
                    numbers = ''.join(filter(str.isdigit, text))
                    # print(numbers)
                    dataModel.addStashResult(numbers)
                elif text.__contains__('号码'):
                    start_index = text.find('号码：')
                    if start_index != -1:
                        number = text[start_index + 3:]
                        dataModel.addStashResult(numbers)
                elif text.__contains__('母码'):
                    start_index = text.find('母码：')
                    if start_index != -1:
                        number = text[start_index + 3:]
                        dataModel.addStashResult(numbers)
                elif text.__contains__('务码'):
                    start_index = text.find('务码：')
                    if start_index != -1:
                        number = text[start_index + 3:]
                        dataModel.addStashResult(numbers)
                elif text.__contains__('粤码'):
                    start_index = text.find('粤码：')
                    if start_index != -1:
                        number = text[start_index + 3:]
                        dataModel.addStashResult(numbers)
 
            progress = (index + 1) * 100 // imageCount
            self.progressUpdated.emit(progress)
        self.batchFinished.emit()
        print("RecognitionsAction 识别完成")