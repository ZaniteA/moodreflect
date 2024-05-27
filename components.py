from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon, QPainter, QPolygon, QPixmap
from PyQt6.QtCore import Qt, QPoint



class PlayButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet(self.default_stylesheet())
        self.setIcon(self.create_icon())
        self.setIconSize(self.size())
        
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def default_stylesheet(self):
        return """
        QPushButton {
            border: none;
            background-color: #AC3ACF;
            border-radius: 20;
        }
        QPushButton:hover {
            background-color: #C064DC;
        }
        """

    def create_icon(self):
        size = self.size()
        pixmap = QIcon()
        icon = QPixmap(size)
        icon.fill(Qt.GlobalColor.transparent)

        painter = QPainter(icon)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(Qt.GlobalColor.white)
        painter.setPen(Qt.GlobalColor.white)
        points = [
            QPoint(int(size.width() * 0.35), int(size.height() * 0.2)),
            QPoint(int(size.width() * 0.75), int(size.height() * 0.5)),
            QPoint(int(size.width() * 0.35), int(size.height() * 0.8))
        ]
        triangle = QPolygon(points)
        painter.drawPolygon(triangle)
        painter.end()

        pixmap.addPixmap(icon)
        return QIcon(icon)


'''
class PlayButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedSize(50, 50)
        self.setStyleSheet("background-color: white; border: none;")
        self.default_color = QColor(128, 0, 128)  # Purple
        self.hover_color = QColor(191, 64, 191)  # Lighter purple
        self.current_color = self.default_color
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def enterEvent(self, event):
        self.current_color = self.hover_color
        self.update()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.current_color = self.default_color
        self.update()
        super().leaveEvent(event)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(self.current_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(0, 0, self.width(), self.height())
        super().paintEvent(event)

    def sizeHint(self):
        return QSize(50, 50)
'''