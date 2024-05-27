import datetime
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame, QPushButton
from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput

import configs
from components import PlayButton



class HomePage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)

        self.setAutoFillBackground(True)

        self.init_ui()

    
    def init_ui(self):
        self.setStyleSheet('background-color: #1E1E1E;')

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.greeting_label = QLabel(self.get_greeting())
        self.greeting_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.greeting_label.setFont(self.parent.getSizedFont(configs.H1_FONT_SIZE))
        self.layout.addWidget(self.greeting_label)

        self.records_area = QScrollArea()
        self.records_area.setWidgetResizable(True)
        self.records_area.setStyleSheet('''
            QScrollBar:vertical {
                background-color: black;
            }
            
            QScrollBar::handle:vertical {
                background-color: #777;
            }
        ''')
        self.layout.addWidget(self.records_area)
        self.refresh_records()


    def refresh_records(self):
        self.clear_item(self.records_area)

        self.records_container = QWidget()
        self.records_layout = QVBoxLayout()
        self.records_container.setLayout(self.records_layout)
        self.records_area.setWidget(self.records_container)

        self.display_records()


    def clear_item(self, item):
        if hasattr(item, "layout"):
            if callable(item.layout):
                layout = item.layout()
        else:
            layout = None

        if hasattr(item, "widget"):
            if callable(item.widget):
                widget = item.widget()
        else:
            widget = None

        if widget:
            widget.setParent(None)
        elif layout:
            for i in reversed(range(layout.count())):
                self.clear_item(layout.itemAt(i))


    def get_greeting(self):
        current_hour = datetime.datetime.now().hour
        if current_hour < 12:
            return "Good morning"
        elif 12 <= current_hour < 18:
            return "Good afternoon"
        else:
            return "Good evening"


    def display_records(self):
        records = reversed(self.parent.mood_manager.read_history())

        self.audio_players = []
        self.audio_outputs = []
        self.play_buttons = []
        for record in records:
            card = self.create_record_card(record)
            self.records_layout.addWidget(card)

        self.records_layout.addStretch()


    def parseTimestamp(self, timestamp):
        return datetime.datetime.strptime(timestamp, '%Y%m%d_%H%M%S').strftime('%d %b %Y %H:%M')


    def create_record_card(self, record):
        card = QFrame()
        card.setFrameShape(QFrame.Shape.Box)
        card.setStyleSheet("background-color: #333; color: white;")
        card_layout = QVBoxLayout()
        card.setLayout(card_layout)

        mood_label = QLabel('<b>{}</b>'.format(record['mood']))
        mood_label.setFont(self.parent.getSizedFont(configs.H3_FONT_SIZE))
        card_layout.addWidget(mood_label)

        timestamp_label = QLabel(self.parseTimestamp(record['timestamp']))
        timestamp_label.setFont(self.parent.getSizedFont(configs.H4_FONT_SIZE))
        card_layout.addWidget(timestamp_label)

        if record['notes']:
            notes_label = QLabel(record['notes'])
            notes_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
            card_layout.addWidget(notes_label)

        if record['audio']:
            self.audio_players.append(QMediaPlayer())
            self.audio_outputs.append(QAudioOutput())
            self.audio_players[-1].setAudioOutput(self.audio_outputs[-1])
            self.audio_players[-1].setSource(QUrl.fromLocalFile(record['audio']))
            self.audio_outputs[-1].setVolume(50)
            # self.audio_players[-1].play()

            self.play_buttons.append(PlayButton(self))
            self.play_buttons[-1].clicked.connect(self.audio_players[-1].play)
            card_layout.addWidget(self.play_buttons[-1], 0, Qt.AlignmentFlag.AlignRight)

        return card
