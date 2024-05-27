import os
import json

import configs



class MoodManager(object):
    def __init__(self):
        self.data_file = os.path.join(configs.DATA_DIR, configs.DATA_FILE_NAME)
        self._check_data_file()


    def _check_data_file(self):
        if os.path.exists(self.data_file):
            pass
        else:
            try:
                fresh_data = {'history': []}
                with open(self.data_file, 'w') as dtf:
                    json.dump(fresh_data, dtf)
            except Exception:
                self.logger.log('Error opening data file:')


    def append_mood(self, timestamp, audio, notes, mood):
        try:
            with open(self.data_file, 'r') as dtf:
                data = json.load(dtf)
        except Exception:
            self.logger.log('Error opening data file:')
            return
        
        if audio is None:
            audio = ''

        data['history'].append({
            'timestamp': timestamp,
            'audio': audio,
            'notes': notes,
            'mood': mood
        })

        try:
            with open(self.data_file, 'w') as dtf:
                json.dump(data, dtf)
        except Exception:
            self.logger.log('Error opening data file:')
            return
        
    
    def read_history(self):
        try:
            with open(self.data_file, 'r') as dtf:
                data = json.load(dtf)
        except Exception:
            self.logger.log('Error opening data file:')
            return
        
        return data['history']
