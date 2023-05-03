import logging

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    def __init__(self):
        pass

    def log_info(self, message):
        logging.info(message)

    def log_error(self, message):
        logging.error(message)

