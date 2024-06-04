from PyQt6.QtWidgets import QMainWindow, QWidget, QHBoxLayout, QListWidget, QListWidgetItem, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontDatabase, QFont

from components import DropShadow
import configs
import utilities
from logger import Logger
from mood_manager import MoodManager
from models import AIModelManager
from home import HomePage
from new_mood import NewMoodPage
from stats import StatisticsPage
from about import AboutPage



class MoodReflectApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.logger = Logger()
        self.mood_manager = MoodManager(self)
        self.ai_model = AIModelManager()
        self.init_ui()


    def importFont(self, font_path: str) -> QFont:
        # Try importing custom font
        fallback_font_family = configs.FALLBACK_FONT
        try:
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id < 0:
                self.logger.log('Error loading font:')
                return QFont(fallback_font_family)
            else:
                return QFont(QFontDatabase.applicationFontFamilies(font_id)[0])
        except (FileNotFoundError, PermissionError):
            self.logger.log('Font file not found:')
            return QFont(fallback_font_family)


    def show(self):
        super().show()
        self.showMaximized()


    def heading_font(self, points) -> QFont:
        sized_font = self.heading_font_object
        sized_font.setPointSize(points)
        return sized_font
                

    def body_font(self, points) -> QFont:
        sized_font = self.body_font_object
        sized_font.setPointSize(points)
        return sized_font
    

    def bold_body_font(self, points) -> QFont:
        sized_font = self.bold_body_font_object
        sized_font.setPointSize(points)
        return sized_font


    def init_ui(self):
        self.setWindowTitle('MoodReflect')

        # Fonts
        self.heading_font_object   = self.importFont(utilities.adjust_path('assets/fonts/Manrope-Regular.ttf'))
        self.body_font_object      = self.importFont(utilities.adjust_path('assets/fonts/SourceSans3-Regular.ttf'))
        self.bold_body_font_object = self.importFont(utilities.adjust_path('assets/fonts/SourceSans3-Bold.ttf'))

        # Main widget
        main_widget = QWidget()
        main_widget.setObjectName('MainWidget')
        main_widget.setStyleSheet(f'QWidget#MainWidget {{ background-color: {configs.BACKGROUND_COLOR}; }}')
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_widget.setLayout(main_layout)

        # Sidebar
        self.sidebar = QListWidget()
        self.sidebar.setFixedWidth(250)
        self.sidebar.setViewportMargins(12, 50, 12, 50)
        self.sidebar.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.sidebar.setSpacing(10)
        DropShadow().apply_effect(self.sidebar)
        self.sidebar.setFont(self.heading_font(configs.H4_FONT_SIZE))
        self.sidebar.setStyleSheet(f'''
            QListWidget {{
                background-color: {configs.MEDIUM_COLOR_1};
                color: white;
            }}
            QListWidget::item {{
                padding: 8px 20px;
                border-radius: 8px;
            }}
            QListWidget::item:selected {{
                background-color: {configs.LIGHT_COLOR_1};
                color: black;
            }}
        ''')

        # Sidebar items
        home_item = QListWidgetItem('Home')
        new_mood_item = QListWidgetItem('New Mood')
        stats_item = QListWidgetItem('Statistics')
        about_item = QListWidgetItem('About')
        self.sidebar.addItem(home_item)
        self.sidebar.addItem(new_mood_item)
        self.sidebar.addItem(stats_item)
        self.sidebar.addItem(about_item)
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

        # Stats screen
        self.stats_screen = StatisticsPage(self)
        self.stack.addWidget(self.stats_screen)

        # About screen
        self.about_screen = AboutPage(self)
        self.stack.addWidget(self.about_screen)

        # Set initial screen
        self.sidebar.setCurrentRow(0)


    def display_content(self, current):
        if not current:
            return
        
        index = self.sidebar.row(current)
        self.stack.setCurrentIndex(index)
        if index == 0:
            self.home_screen.refresh()
        elif index == 2:
            self.stats_screen.refresh()