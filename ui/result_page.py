from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLabel, QMessageBox, QSpinBox, QDialog, QListWidgetItem
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, Signal
from model.data_model import DataModel

class RecogResultItem:
    def __init__(self, imgIndex, originCode, digitCode, errorGroup):
        self.imgIndex = imgIndex
        self.originCode = originCode
        self.digitCode = digitCode
        self.errorGroup = errorGroup
    
    def __str__(self):
        if len(self.errorGroup) > 0:
            return f"{self.originCode} {self.errorGroup}"
        else:
            return f"{self.originCode}"

class ResultPage(QWidget):
    signal_pre_step = Signal()
    signal_check_result_done = Signal()
    
    def __init__(self, dataModelMap):
        super().__init__()
        self.dataModelMap = dataModelMap
        self.initUI()
        self.loadData()
    
    def initUI(self):
        pageLayout = QVBoxLayout()  # 创建水平布局
        self.setLayout(pageLayout) 

        operateBox = QHBoxLayout()
        # 临界值标签
        criticalValueLabel = QLabel("临界值:") 
        operateBox.addWidget(criticalValueLabel)

        # 阈值设定
        self.sbDiffValue = QSpinBox()
        self.sbDiffValue.setRange(1, 5000)
        self.sbDiffValue.setValue(50)
        operateBox.addWidget(self.sbDiffValue)

        # 开始检测
        btnCheckResult = QPushButton("检测结果")
        btnCheckResult.clicked.connect(self.checkRecogResult)
        operateBox.addWidget(btnCheckResult)

        # 上一步
        btnPreStep = QPushButton("上一步")
        btnPreStep.clicked.connect(self.on_pre_step)
        operateBox.addWidget(btnPreStep)

        # 结束检测
        btnNewRound = QPushButton("新一轮检测")
        btnNewRound.clicked.connect(self.newRound)
        operateBox.addWidget(btnNewRound)

        pageLayout.addLayout(operateBox)

        contentLayout = QHBoxLayout()
        pageLayout.addLayout(contentLayout)
        
        # 左边布局 - 图片列表
        leftLayout = QVBoxLayout()
        contentLayout.addLayout(leftLayout)
        
        self.imageList = QListWidget()
        self.imageList.currentTextChanged.connect(self.on_image_selected)
        leftLayout.addWidget(self.imageList)
        
        # 右边布局 - 识别结果
        rightLayout = QVBoxLayout()
        contentLayout.addLayout(rightLayout)

        self.recogResultList = QListWidget()
        rightLayout.addWidget(self.recogResultList)


    # 加载数据
    def loadData(self):
        print("加载数据")
        self.imageList.clear()
        self.recogResultList.clear()

        self.imageList.addItem("All")
        for index, dataModel in self.dataModelMap.items():
            self.imageList.addItem(str(dataModel.index))

            for recogResult in dataModel.stashResultList:
                digitCode = int(recogResult.lstrip('0') or '0')
                listItemData = RecogResultItem(dataModel.index, recogResult, digitCode, [])
                listItem = QListWidgetItem(str(listItemData))
                listItem.setData(Qt.UserRole, listItemData)
                self.recogResultList.addItem(listItem)

    # 检测数据
    def checkRecogResult(self):
        print("checkRecogResult")
        diffValue = self.sbDiffValue.value()
        if diffValue <= 0:
            QMessageBox.warning(self, "异常", "请设定合理的临界值")
            return
        
        newCodeMap = {}
        for i in range(self.recogResultList.count()):
            item = self.recogResultList.item(i)
            itemData = item.data(Qt.UserRole)
            # print("get item data: " + str(itemData))
            newCodeMap[itemData.digitCode] = itemData
        
        newSortedCodes = sorted(newCodeMap.keys())
        hasError = False
        for i in range(len(newSortedCodes) - 1):
            item1 = newSortedCodes[i]
            item2 = newSortedCodes[i + 1]

            originItem1 = newCodeMap[item1].originCode
            originItem2 = newCodeMap[item2].originCode
            
            # 这里假设item1和item2都是数字，你可以根据实际情况修改
            diff = abs(item1 - item2)
            print(f"比较数值: {item1} 和 {item2}, diff: {diff}")
            if diff < diffValue:
                QMessageBox.warning(self, "错误", f"发现相邻号码差值小于{diffValue}, 号码: {originItem1} 和 {originItem2}")
                
                # 为重复的号码添加标记
                for ri in range(self.recogResultList.count()):
                    item = self.recogResultList.item(ri)
                    if item.text() == originItem1:
                        item.data(Qt.UserRole).errorGroup.append(i)
                        item.setText(str(item.data(Qt.UserRole)))
                    elif item.text() == originItem2:
                        item.data(Qt.UserRole).errorGroup.append(i)
                        item.setText(str(item.data(Qt.UserRole)))
                
                hasError = True
        
        if not hasError:
            QMessageBox.information(self, "校验通过", "未发现异常号码")


    def newRound(self):
        print("newRound")
        self.signal_check_result_done.emit()


    def on_image_selected(self, text):
        if text == "All":
            for i in range(self.recogResultList.count()):
                self.recogResultList.item(i).setForeground(Qt.black)
        else:
            for i in range(self.recogResultList.count()):
                item = self.recogResultList.item(i)
                itemData = item.data(Qt.UserRole)
                if str(itemData.imgIndex) == text:
                    item.setForeground(Qt.red)
                else:
                    item.setForeground(Qt.black)


    def on_error_item_selected(self, text):
        if text == "-------":
            return
        
        print("on_error_item_selected: " + text)
        targetDataModel = None
        for itemDataModel in self.dataModelMap.values():
            if text in itemDataModel.stashResultList:
                print("itemDataModel.index: " + str(itemDataModel.index))
                targetDataModel = itemDataModel
                break

        print("弹出一个窗口展示图片")
        dialog = QDialog(self)
        dialog.resize(800, 600)
        layout = QVBoxLayout(dialog)
        label = QLabel(dialog)
        layout.addWidget(label)
        pixmap = QPixmap(targetDataModel.targetImage)
        label.setPixmap(pixmap)
        dialog.exec_()
        
    def on_pre_step(self):
        print("on_pre_step")
        self.signal_pre_step.emit()