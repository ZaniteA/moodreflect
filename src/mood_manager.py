import os
import json
import datetime

import configs
import utilities



class Mood(object):
    def __init__(self, timestamp: str = None, audio: str = None,
                 notes: str = None, mood: str = None):
        self.timestamp = timestamp
        self.audio     = audio
        self.notes     = notes
        self.mood      = mood


    def from_dict(self, orig_dict: dict):
        self.timestamp = orig_dict['timestamp']
        self.audio     = orig_dict['audio']
        self.notes     = orig_dict['notes']
        self.mood      = orig_dict['mood']


    def to_dict(self) -> dict:
        return {
            'timestamp': self.timestamp,
            'audio'    : self.audio,
            'notes'    : self.notes,
            'mood'     : self.mood
        }



class MoodManager(object):
    def __init__(self, parent):
        self.parent = parent
        self.data_file = utilities.adjust_path(os.path.join(configs.DATA_DIR, configs.DATA_FILE_NAME))
        self.check_data_file()


    def check_data_file(self):
        if os.path.exists(self.data_file):
            pass
        else:
            try:
                fresh_data = {'history': []}
                with open(self.data_file, 'w') as dtf:
                    json.dump(fresh_data, dtf, indent=4)
            except Exception:
                self.parent.logger.log('Error opening data file:')


    def ensure_sorted(self, data: dict) -> dict:
        data['history'] = sorted(data['history'], key=lambda entry: entry['timestamp'])
        return data


    def read_data(self) -> dict:
        try:
            with open(self.data_file, 'r') as dtf:
                data = json.load(dtf)
                # return data
                return self.ensure_sorted(data)
        except Exception:
            self.parent.logger.log('Error opening data file:')
            return None
        
    
    def write_data(self, data: dict):
        # data = self.ensure_sorted(data)
        try:
            with open(self.data_file, 'w') as dtf:
                json.dump(data, dtf, indent=4)
        except Exception:
            self.parent.logger.log('Error opening data file:')
            return


    def append_mood(self, mood: Mood):
        data = self.read_data()
        if data is None:
            return
        data['history'].append(mood.to_dict())
        self.write_data(data)
        
    
    def read_history(self) -> list[Mood]:
        data = self.read_data()
        if data is None:
            return None
        
        moods = []
        for entry in data['history']:
            moods.append(Mood())
            moods[-1].from_dict(entry)
        return moods


    def get_monthly_history(self, month: int, year: int) -> list[Mood]:
        data = self.read_history()
        filtered_data = []
        for entry in data:
            entry_time = datetime.datetime.strptime(entry.timestamp, configs.FILE_TIME_FORMAT)
            if entry_time.month == month and entry_time.year == year:
                filtered_data.append(entry)
        return filtered_data
