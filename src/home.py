import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import configs
from components import PlayButton, DropShadow
from mood_manager import Mood
import utilities



class HomePage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)
        self.init_ui()

    
    def init_ui(self):
        self.setStyleSheet('background-color: none;')

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 20, 0, 0)
        self.setLayout(self.layout)

        # Greeting
        self.greeting_label = QLabel(self.get_greeting())
        self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greeting_label.setFont(self.parent.heading_font(configs.H1_FONT_SIZE))
        self.greeting_label.setStyleSheet('color: black;')
        self.layout.addWidget(self.greeting_label)

        self.layout.addSpacing(10)

        # Records
        self.records_area = QScrollArea()
        self.records_area.setViewportMargins(20, 0, 20, 0)
        self.records_area.setWidgetResizable(True)
        self.records_area.setStyleSheet(f'''
            QScrollArea {{
                background-color: {configs.BACKGROUND_COLOR};
            }}

            QScrollBar:vertical {{
                background-color: {configs.BACKGROUND_COLOR};
            }}
            
            QScrollBar::handle:vertical {{
                background-color: {configs.MEDIUM_COLOR_1};
            }}
        ''')
        self.layout.addWidget(self.records_area)
        self.refresh()


    def get_greeting(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return 'Good morning!'
        elif 12 <= current_hour < 18:
            return 'Good afternoon!'
        else:
            return 'Good evening!'


    def refresh(self):
        utilities.clear_item(self.records_area)

        self.records_container = QWidget()
        self.records_container.setStyleSheet(f'background-color: {configs.BACKGROUND_COLOR};')
        self.records_layout = QVBoxLayout()
        self.records_container.setLayout(self.records_layout)
        self.records_area.setWidget(self.records_container)

        self.display_records()


    def display_records(self):
        records = reversed(self.parent.mood_manager.read_history())
        self.parent.logger.log(records)

        self.audio_players = []
        self.audio_outputs = []
        self.play_buttons = []

        first = True
        for record in records:
            if not first:
                self.records_layout.addSpacing(12)

            card = self.create_record_card(record)
            self.records_layout.addWidget(card)
            first = False

        self.records_layout.addStretch()


    def parseTimestamp(self, timestamp):
        return (datetime.datetime.strptime(timestamp, configs.FILE_TIME_FORMAT)
                                 .strftime(configs.CARD_TIME_FORMAT))


    def create_record_card(self, record: Mood):
        # Card
        card = QFrame()
        card.setFrameShape(QFrame.Shape.Box)
        card.setContentsMargins(8, 8, 8, 8)
        card.setStyleSheet(f'''
            QFrame {{
                background-color: {configs.MOOD_COLORS[record.mood][0].name()};
                color: black;
                border-radius: 10px;
            }}
        ''')
        DropShadow().apply_effect(card)
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        # Title
        mood_label = QLabel('<b>{}</b>'.format(record.mood))
        mood_label.setFont(self.parent.heading_font(configs.H3_FONT_SIZE))
        card_layout.addWidget(mood_label)

        # Timestamp
        timestamp_label = QLabel(self.parseTimestamp(record.timestamp))
        timestamp_label.setFont(self.parent.body_font(configs.H4_FONT_SIZE))
        card_layout.addWidget(timestamp_label)

        # Notes
        if record.notes:
            notes_label = QLabel(record.notes)
            notes_label.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
            notes_label.setWordWrap(True)
            card_layout.addWidget(notes_label)

        # Audio
        if record.audio:
            self.audio_players.append(QMediaPlayer())
            self.audio_outputs.append(QAudioOutput())
            self.audio_players[-1].setAudioOutput(self.audio_outputs[-1])
            self.audio_players[-1].setSource(QUrl.fromLocalFile(record.audio))
            self.audio_outputs[-1].setVolume(50)

            self.play_buttons.append(PlayButton(self))
            self.play_buttons[-1].clicked.connect(self.audio_players[-1].play)
            card_layout.addWidget(self.play_buttons[-1], 0, Qt.AlignmentFlag.AlignRight)

        return card
