
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
        
    def addStashResult(self, stashResult):
        if len(stashResult) > 8:
            stashResult = stashResult[:8] 
        self.stashResultList.append(stashResult)
        
    def editStashResult(self, oldResult, newResult):
        for i, resultItem in enumerate(self.stashResultList):
            if resultItem == oldResult:
                self.stashResultList[i] = newResult

    def removeStashResult(self, delItem):
        self.stashResultList.remove(delItem)
        
    def cleanAll(self):
        self.stashResultList.clear()
        
        
    