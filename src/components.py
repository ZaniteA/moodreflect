from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QLabel
from PyQt6.QtGui import QIcon, QPainter, QPolygon, QPixmap
from PyQt6.QtCore import Qt, QPoint

import configs



class PlayButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet(f'''
            QPushButton {{
                border: none;
                background-color: {configs.MEDIUM_COLOR_1};
                border-radius: 20;
            }}
            QPushButton:hover {{
                background-color: {configs.MEDIUM_COLOR_2};
            }}
        ''')
        self.setIcon(self.create_icon())
        self.setIconSize(self.size())
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        DropShadow().apply_effect(self)


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
            QPoint(int(size.width() * 0.4), int(size.height() * 0.275)),
            QPoint(int(size.width() * 0.7), int(size.height() * 0.5)),
            QPoint(int(size.width() * 0.4), int(size.height() * 0.725))
        ]
        triangle = QPolygon(points)
        painter.drawPolygon(triangle)
        painter.end()

        pixmap.addPixmap(icon)
        return QIcon(icon)



class TextButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(f'''
            QPushButton {{
                border-radius: 10px;
                padding: 4px;
                background-color: {configs.MEDIUM_COLOR_1};
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {configs.MEDIUM_COLOR_2};
            }}
        ''')
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        DropShadow().apply_effect(self)



class NavigationButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet(f'''
            QPushButton {{
                border-radius: 15px;
                background-color: {configs.MEDIUM_COLOR_1};
                color: white;
                border: none;
            }}
            QPushButton:hover {{
                background-color: {configs.MEDIUM_COLOR_2};
            }}
            QPushButton:disabled {{
                background-color: {configs.DISABLED_COLOR};
            }}
        ''')
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        DropShadow().apply_effect(self)



class DropShadow(object):
    def __init__(self):
        self.shadow_effect = QGraphicsDropShadowEffect()
        self.shadow_effect.setColor(configs.SHADOW_COLOR)
        self.shadow_effect.setBlurRadius(18)
        self.shadow_effect.setOffset(0, 0)

    
    def apply_effect(self, target):
        target.setGraphicsEffect(self.shadow_effect)



class AboutPageText(QLabel):
    def __init__(self, text):
        super().__init__(text)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet('color: black;')
