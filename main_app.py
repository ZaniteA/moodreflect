from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget
from PyQt6.QtGui import QFontDatabase, QFont

import configs
from logger import Logger
from mood_manager import MoodManager
from home import HomePage
from new_mood import NewMoodPage



class MoodReflectApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.mood_manager = MoodManager()
        self.init_ui()


    def _importFont(self):
        # Try importing custom font
        fallback_font_family = 'Arial'
        try:
            font_id = QFontDatabase.addApplicationFont('assets/fonts/Manrope-Regular.ttf')
            if font_id < 0:
                self.logger.log('Error loading font:')
                return QFont(fallback_font_family)
            else:
                return QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
        except (FileNotFoundError, PermissionError):
            self.logger.log('Font file not found:')
            return QFont(fallback_font_family)
        

    def getSizedFont(self, points):
        sized_font = self.font
        sized_font.setPointSize(points)
        return sized_font


    def show(self):
        super().show()
        self.showMaximized()


    def init_ui(self):
        self.setWindowTitle('MoodReflect')
        self.font = self._importFont()

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setSpacing(10)
        self.sidebar.setFont(self.getSizedFont(configs.BODY_FONT_SIZE))
        self.sidebar.setStyleSheet('''
            QListWidget {
                background-color: #333;
                color: white;
            }
            QListWidget::item {
                padding: 5px;
            }
            QListWidget::item:selected {
                background-color: #555;
            }
        ''')

        home_item = QListWidgetItem('Home')
        new_mood_item = QListWidgetItem('New Mood')
        self.sidebar.addItem(home_item)
        self.sidebar.addItem(new_mood_item)
        self.sidebar.currentItemChanged.connect(self.display_content)

        main_layout.addWidget(self.sidebar)

        # Content area
        self.stack = QStackedWidget()
        main_layout.addWidget(self.stack)

        # Home screen
        self.home_screen = HomePage(self)
        self.stack.addWidget(self.home_screen)

        # New Mood screen
        self.new_mood_screen = NewMoodPage(self)
        self.stack.addWidget(self.new_mood_screen)

        # Set initial screen
        self.sidebar.setCurrentRow(0)


    def display_content(self, current):
        if not current:
            return
        index = self.sidebar.row(current)
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.home_screen.refresh_records()  # Refresh the home screen when navigating to it