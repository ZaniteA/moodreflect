import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import datetime
import random
import os
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import QTimer

import configs



class NewMoodPage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)

        self.setAutoFillBackground(True)
        # self.setStyleSheet('background-color: white;')
        self.init_ui()

        self.is_recording = False
        self.sample_rate = 44100  # Sample rate
        self.recorded_data = []
        self.moods = ['Happy', 'Sad', 'Anxious', 'Shocked', 'Relaxed', 'Angry']


    def init_ui(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Recorder controls
        self.recorder_layout = QHBoxLayout()

        self.record_button = QPushButton('Start Recording')
        self.record_button.setFixedWidth(150)
        self.record_button.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.record_button.clicked.connect(self.toggle_recording)
        self.recorder_layout.addWidget(self.record_button)

        self.status_label = QLabel('Status: Not Recording')
        self.status_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.status_label.setStyleSheet('color: white;')
        self.recorder_layout.addWidget(self.status_label)

        self.layout.addLayout(self.recorder_layout)

        # Text box for notes
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.notes_text_edit.setPlaceholderText('Enter your notes here...')
        self.notes_text_edit.setFixedHeight(200)
        self.layout.addWidget(self.notes_text_edit)

        # Predict button and label
        self.predict_layout = QHBoxLayout()
        self.predict_label = QLabel("When you're done, click this:")
        self.predict_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.predict_label.setStyleSheet('color: white;')
        self.predict_layout.addWidget(self.predict_label)
        
        self.predict_button = QPushButton('Predict')
        self.predict_button.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.predict_button.clicked.connect(self.predict_mood)
        self.predict_layout.addWidget(self.predict_button)
        
        self.layout.addLayout(self.predict_layout)

        self.layout.insertSpacing(3, 50)

        # Placeholder for mood label and save button
        self.result_layout = QVBoxLayout()
        self.layout.addLayout(self.result_layout)

        self.layout.addStretch()


    def toggle_recording(self):
        if not self.is_recording:
            self.start_recording()
        else:
            self.stop_recording()


    def start_recording(self):
        if self.recorded_data:
            reply = QMessageBox.question(self, 'Overwrite Recording',
                                         'Starting a new recording will overwrite the existing one. Do you want to continue?',
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        self.is_recording = True
        self.recorded_data = []
        self.record_button.setText('Stop Recording')
        self.status_label.setText('Status: Recording...')
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.record_audio)
        self.timer.start(2000)  # Record in chunks of 100 ms


    def record_audio(self):
        data = sd.rec(int(2 * self.sample_rate), samplerate=self.sample_rate, channels=1, blocking=True)
        self.recorded_data.append(data)


    def stop_recording(self):
        self.is_recording = False
        self.record_button.setText('Start Recording')
        self.status_label.setText('Status: Finished recording')
        self.timer.stop()


    def save_recording(self):
        if not self.recorded_data and not self.notes_text_edit.toPlainText():
            self.status_label.setText('Status: Nothing to save')
            return

        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        
        audio_file_path = None
        if self.recorded_data:
            audio_file_path = os.path.join(configs.DATA_DIR,
                                           'recording_{}.wav'.format(timestamp))
            data = np.concatenate(self.recorded_data)
            for t in data:
                logging.error(t)
            wavfile.write(audio_file_path, self.sample_rate, data)

        self.parent.mood_manager.append_mood(timestamp=timestamp,
                                             audio=audio_file_path,
                                             notes=self.notes_text_edit.toPlainText(),
                                             mood=self.current_mood)
            
        self.status_label.setText('Status: Mood saved successfully')

        # Clear stored data
        self.recorded_data = []
        self.notes_text_edit.clear()
        self.clear_results()


    def clear_results(self):
        # Clear any existing results
        self.current_mood = None
        for i in reversed(range(self.result_layout.count())): 
            widget = self.result_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()


    def predict_mood(self):
        self.clear_results()

        # Check if inputs are empty
        if not self.recorded_data and not self.notes_text_edit.toPlainText():
            no_input_label = QLabel('Please input audio or text to predict your mood')
            no_input_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
            no_input_label.setStyleSheet('color: white;')
            self.result_layout.addWidget(no_input_label)
            return
        
        # Check if user is still recording
        if self.is_recording:
            still_recording_label = QLabel('Please stop recording before predicting your mood')
            still_recording_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
            still_recording_label.setStyleSheet('color: white;')
            self.result_layout.addWidget(still_recording_label)
            return

        # Pick a random mood
        self.current_mood = random.choice(self.moods)
        mood_label = QLabel('Your mood is: <b>{}</b>'.format(self.current_mood))
        mood_label.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        mood_label.setStyleSheet('color: white;')
        self.result_layout.addWidget(mood_label)

        # Add save button
        self.save_button = QPushButton('Save')
        self.save_button.setFont(self.parent.getSizedFont(configs.BODY_FONT_SIZE))
        self.save_button.clicked.connect(self.save_recording)
        self.result_layout.addWidget(self.save_button)
