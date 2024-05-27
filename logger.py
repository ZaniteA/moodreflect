import logging

import configs



class Logger(object):
    def __init__(self):
        logging.basicConfig(filename=configs.LOG_FILE_NAME, level=logging.DEBUG)

        # Clear log file
        open(configs.LOG_FILE_NAME, 'w')
        

    def log(msg):
        logging.error(msg, exc_info=True)
