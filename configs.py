import os
from PyQt6.QtGui import QColor



# File names
LOG_FILE_NAME   = 'moodreflect.log'
DATA_DIR        = os.path.join('assets', 'data')
DATA_FILE_NAME  = 'history.dat'
TEMP_AUDIO_FILE = 'tmp.wav'


# Recording
TIME_CHUNK_MS = 2000
TIME_CHUNK_S  = TIME_CHUNK_MS // 1000


# Fonts
FALLBACK_FONT  = 'Arial'
H1_FONT_SIZE   = 30
H2_FONT_SIZE   = 20
H3_FONT_SIZE   = 16
H4_FONT_SIZE   = 14
BODY_FONT_SIZE = 12


# Colors
BACKGROUND_COLOR = '#FFF1F1'
LIGHT_COLOR_1    = '#EAC4E5'
MEDIUM_COLOR_1   = '#9855C5'
MEDIUM_COLOR_2   = '#B57BDD'
DISABLED_COLOR   = '#D1BFCB'
MEDIUM_COLOR_1_QCOLOR = QColor(152,  85, 197)
DARK_GRAY_QCOLOR      = QColor(143, 144, 142)
SHADOW_COLOR          = QColor(171, 171, 171)


# Statistics screen
TABLE_PADDING      = 5
NONZERO_TICK_COUNT = 6


# Date and time
FILE_TIME_FORMAT  = '%Y%m%d_%H%M%S'
CARD_TIME_FORMAT  = '%d %b %Y %H:%M'
STATS_TIME_FORMAT = '%B %Y'


# App information
APP_NAME       = 'MoodReflect'
APP_VERSION    = 'v1.0'
APP_DETAILS    = 'A mood tracker app made as a Software Engineering project in BINUS University.'
APP_AUTHOR_ORG = 'LE01 Group 7'
APP_AUTHORS    = [
    '2602069596 • Jack Julius Ryadi Lie',
    '2602078726 • Albert Yulius Ramahalim',
    '2602081462 • Christopher Alexander Chandra',
    '2602082944 • Christoffer Edbert Karuniawan'
]


# Moods
MOODS          = ["Neutral", "Happy", "Sad", "Angry", "Fear", "Disgust", "Surprise"]
ENCOURAGEMENTS = {
    'Empty'   : "You haven't tracked your moods yet that month!",
    'Neutral' : "How about we explore some interesting options today?",
    'Happy'   : "Let's keep this positive energy flowing!",
    'Sad'     : "It's okay to feel this way. Take your time and you'll feel better soon.",
    'Angry'   : "Take a step back and express yourself calmly when you're ready.",
    'Fear'    : "You are braver than you think. Let's face this together.",
    'Disgust' : "Let's move on from the unpleasantness.",
    'Surprise': "Wow! Let's see where this unexpected turn takes us.",
}
MOOD_COLORS    = {
    'Neutral' : [QColor(228, 228, 228), QColor(144, 149, 158), QColor(104, 109, 118)],
    'Happy'   : [QColor(251, 245, 207), QColor(255, 217,  55), QColor(242, 179,   0)],
    'Sad'     : [QColor(207, 229, 231), QColor( 19, 106, 149), QColor(  0,  54,  94)],
    'Angry'   : [QColor(255, 222, 197), QColor(250, 122, 122), QColor(252,  65,   0)],
    'Fear'    : [QColor(215, 245, 217), QColor(106, 188, 104), QColor( 90, 136, 100)],
    'Disgust' : [QColor(254, 229, 178), QColor(166, 123,  91), QColor(111,  78,  55)],
    'Surprise': [QColor(250, 205, 255), QColor(182, 114, 200), QColor(134,  70, 156)],
}



# AI
TEXT_WEIGHT   = 1
SPEECH_WEIGHT = 5
RESULT_TO_LABEL = {
    0 : 'Angry',
    1 : 'Disgust',
    2 : 'Fear',
    3 : 'Happy',
    4 : 'Neutral',
    5 : 'Sad',
    6 : 'Suprise'
}