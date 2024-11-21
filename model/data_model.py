
# 一张图的关联的数据
class DataModel:
    
    def __init__(self, index, targetImage):
        super().__init__()
        
        # 图片序号
        self.index = index

        # 图片列表
        self.targetImage = targetImage
        
        # 暂存识别结果列表
        self.stashResultList = []
        
        # 最终识别结果列表
        self.finalResultList = []
        
    def addStashResult(self, stashResult):
        self.stashResultList.append(stashResult)
        
    def editStashResult(self, oldResult, newResult):
        for i, resultItem in enumerate(self.stashResultList):
            if resultItem == oldResult:
                self.imageList[i] = newResult

    def removeStashResult(self, delItem):
        self.stashResultList.remove(delItem)
        
    def addFinalResult(self, inputResultList):
        self.finalResultList.extend(inputResultList)
        
    def cleanAll(self):
        self.imageList.clear()
        self.stashResultList.clear()
        self.finalResultList.clear()
        
        
    