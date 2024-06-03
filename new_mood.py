import sounddevice as sd
from scipy.io import wavfile
import numpy as np
import datetime
import random
import os
from PyQt6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel, QTextEdit, QMessageBox
from PyQt6.QtCore import Qt, QTimer

import configs
from components import TextButton, DropShadow
from mood_manager import Mood
import utilities



class NewMoodPage(QWidget):
    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(self.parent)

        self.init_ui()

        self.is_recording = False
        self.sample_rate = 22050  # Sample rate
        self.recorded_data = []


    def init_ui(self):
        self.setStyleSheet('background-color: none;')

        self.layout = QVBoxLayout()
        self.setContentsMargins(20, 50, 20, 50)
        self.setLayout(self.layout)

        # Recorder controls
        self.recorder_layout = QHBoxLayout()

        # Start/stop record button
        self.record_button = TextButton('Start Recording')
        self.record_button.setFixedWidth(180)
        self.record_button.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.record_button.clicked.connect(self.toggle_recording)
        self.recorder_layout.addWidget(self.record_button)

        self.recorder_layout.addSpacing(15)

        # Status label
        self.status_label = QLabel()
        self.set_recording_status('Not Recording')
        self.status_label.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.status_label.setStyleSheet('color: black;')
        self.recorder_layout.addWidget(self.status_label)

        self.layout.addLayout(self.recorder_layout)
        self.layout.addSpacing(15)

        # Text box for notes
        self.notes_text_edit = QTextEdit()
        self.notes_text_edit.setStyleSheet(f'''
            background-color: white;
            color: black;
            border-radius: 10px;
            padding: 4px;
                                           
            selection-color: white;
            selection-background-color: {configs.MEDIUM_COLOR_2}
        ''')
        DropShadow().apply_effect(self.notes_text_edit)
        self.notes_text_edit.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.notes_text_edit.setPlaceholderText('Enter your notes here...')
        self.notes_text_edit.setFixedHeight(300)

        self.layout.addWidget(self.notes_text_edit)
        self.layout.addSpacing(15)

        # Predict button and label
        self.predict_layout = QHBoxLayout()
        self.predict_layout.addStretch()
        
        self.predict_button = TextButton('Predict Mood')
        self.predict_button.setFixedWidth(180)
        self.predict_button.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.predict_button.clicked.connect(self.predict_mood)
        self.predict_layout.addWidget(self.predict_button)
        
        self.layout.addLayout(self.predict_layout)
        self.layout.addSpacing(50)

        # Placeholder for mood label and save button
        self.result_layout = QVBoxLayout()
        self.layout.addLayout(self.result_layout)

        self.layout.addStretch()


    def set_recording_status(self, status):
        self.status_label.setText(f'<b>Status:</b> {status}')


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
        self.recorded_data.clear()
        self.record_button.setText('Stop Recording')
        self.set_recording_status('Recording...')
        
        self.stream = sd.InputStream(callback=self.audio_callback, channels=2, samplerate=self.sample_rate)
        self.stream.start()


    def audio_callback(self, indata, frames, time, status):
        self.recorded_data.append(indata.copy())


    def stop_recording(self):
        self.is_recording = False
        self.record_button.setText('Start Recording')
        self.set_recording_status('Finished recording')
        self.stream.stop()


    def save_recording(self,
                       filename: str = os.path.join(configs.DATA_DIR, configs.TEMP_AUDIO_FILE)) -> bool:
        if not self.recorded_data:
            return False
        
        data = np.concatenate(self.recorded_data)
        wavfile.write(filename, self.sample_rate, data)
        return True


    def clear_results(self):
        self.current_mood = None
        utilities.clear_item(self.result_layout)


    def predict_mood(self):
        self.clear_results()

        # Check if inputs are empty
        if not self.recorded_data and not self.notes_text_edit.toPlainText():
            no_input_label = QLabel('Please input audio or text to predict your mood')
            no_input_label.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
            no_input_label.setStyleSheet('color: black;')
            no_input_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_layout.addWidget(no_input_label)
            return
        
        # Check if user is still recording
        if self.is_recording:
            still_recording_label = QLabel('Please stop recording before predicting your mood')
            still_recording_label.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
            still_recording_label.setStyleSheet('color: black;')
            still_recording_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_layout.addWidget(still_recording_label)
            return
        
        # Save audio to temporary file
        audio_file_path = (os.path.join(configs.DATA_DIR, configs.TEMP_AUDIO_FILE)
                           if self.save_recording() else '')
        text = self.notes_text_edit.toPlainText()

        # Predict mood and erase the temporary file
        self.current_mood = self.parent.ai_model.predict(text, audio_file_path)
        os.remove(os.path.join(configs.DATA_DIR, configs.TEMP_AUDIO_FILE))

        mood_label = QLabel('Your mood is: <b>{}</b>'.format(self.current_mood))
        mood_label.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        mood_label.setStyleSheet('color: black;')
        mood_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_layout.addWidget(mood_label)

        # Add save button
        self.save_layout = QHBoxLayout()

        self.save_layout.addStretch()
        self.save_button = TextButton('Save')
        self.save_button.setFixedWidth(180)
        self.save_button.setFont(self.parent.body_font(configs.BODY_FONT_SIZE))
        self.save_button.clicked.connect(self.save_mood)

        self.save_layout.addWidget(self.save_button)
        self.save_layout.addStretch()
        self.result_layout.addLayout(self.save_layout)


    def save_mood(self):
        if not self.recorded_data and not self.notes_text_edit.toPlainText():
            self.set_recording_status('There is no data to save!')
            return

        timestamp = datetime.datetime.now().strftime(configs.FILE_TIME_FORMAT)
        filename = os.path.join(configs.DATA_DIR, f'recording_{timestamp}.wav')
        
        audio_file_path = filename if self.save_recording(filename) else ''

        self.parent.mood_manager.append_mood(Mood(timestamp=timestamp,
                                                  audio=audio_file_path,
                                                  notes=self.notes_text_edit.toPlainText(),
                                                  mood=self.current_mood))
        self.set_recording_status('Mood saved successfully')

        self.recorded_data.clear()
        self.notes_text_edit.clear()
        self.clear_results()
