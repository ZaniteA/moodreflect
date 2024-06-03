import numpy as np
from tensorflow.keras.models import load_model
import pickle
import librosa
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import os

import configs



class SpeechAIModel(object):
    def __init__(self):
        self.model = load_model('assets/models/speech_model.h5')
        with open('assets/models/scaler.pickle', 'rb') as f:
            self.scaler = pickle.load(f)


    def zcr(self, data, frame_length, hop_length):
        zcr = librosa.feature.zero_crossing_rate(y = data,
                                                 frame_length = frame_length,
                                                 hop_length = hop_length)
        return np.squeeze(zcr)


    def rmse(self, data, frame_length = 2048, hop_length = 512):
        rmse = librosa.feature.rms(y = data,
                                   frame_length = frame_length,
                                   hop_length = hop_length)
        return np.squeeze(rmse)


    def mfcc(self, data, sr, frame_length = 2048, hop_length = 512, flatten: bool = True):
        mfcc = librosa.feature.mfcc(y=data, sr=sr)
        return np.squeeze(mfcc.T) if not flatten else np.ravel(mfcc.T)


    def extract_features(self, data, sr = 22050, frame_length = 2048, hop_length = 512):
        result=np.array([])
        result=np.hstack((result,
                          self.zcr(data,frame_length,hop_length),
                          self.rmse(data,frame_length,hop_length),
                          self.mfcc(data,sr,frame_length,hop_length)
                        ))
        return result
    

    def get_predict_feat(self, path):
        d, s_rate = librosa.load(path, duration=2.5, offset=0.6)

        res = self.extract_features(d)
        result = np.array(res)
        result = np.reshape(result, newshape=(1, 2376))

        i_result = self.scaler.transform(result)
        final_result = np.expand_dims(i_result, axis=2)

        return final_result


    def predict_proba(self, path):
        res = self.get_predict_feat(path)
        predictions = self.model.predict(res, verbose=0)
        return predictions



class TextAIModel(object):
    def __init__(self):
        self.model = load_model('assets/models/text_model.hdf5')


    def preprocess(self, data):
        max_words = 1000
        max_len = 150
        tok = Tokenizer(num_words=max_words)
        tok.fit_on_texts(data)
        s1 = tok.texts_to_sequences(data)
        s2 = pad_sequences(s1, maxlen=max_len)
        return s2


    def predict_proba(self, text):
        list_text = [text]
        pre_text = self.preprocess(list_text)
        predictions = self.model.predict(pre_text, verbose=0)
        return predictions



class AIModelManager(object):
    def __init__(self):
        self.text_model   = TextAIModel()
        self.speech_model = SpeechAIModel()


    def predict(self, text,
                audio_file_path = os.path.join(configs.DATA_DIR, configs.TEMP_AUDIO_FILE)):
        prediction = np.zeros((1, len(configs.MOODS)))
        total_weight = 0

        if text:
            prediction += configs.TEXT_WEIGHT * self.text_model.predict_proba(text)
            total_weight += configs.TEXT_WEIGHT

        if audio_file_path:
            prediction += configs.SPEECH_WEIGHT * self.text_model.predict_proba(audio_file_path)
            total_weight += configs.SPEECH_WEIGHT

        prediction /= total_weight

        return configs.RESULT_TO_LABEL[np.argmax(prediction[0])]