from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QDialog
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtCore import Qt

class ImageDialog(QDialog):
    def __init__(self, image_path):
        super().__init__()
        self.setWindowTitle("图片查看")
        
        # 创建图形视图和场景
        self.graphicsView = QGraphicsView(self)
        self.scene = QGraphicsScene(self)
        self.graphicsView.setScene(self.scene)

        # 加载图片
        pixmap = QPixmap(image_path)
        self.imageItem = QGraphicsPixmapItem(pixmap)
        self.scene.addItem(self.imageItem)

        # 设置视图属性
        self.graphicsView.setRenderHint(QPainter.Antialiasing)
        self.graphicsView.setRenderHint(QPainter.SmoothPixmapTransform)
        self.graphicsView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.graphicsView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.graphicsView)
        self.setLayout(layout)

        # 允许放缩
        self.graphicsView.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        # 放缩功能
        factor = 1.2 if event.angleDelta().y() > 0 else 1 / 1.2
        self.graphicsView.scale(factor, factor)