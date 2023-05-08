import logging

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s - %(levelname)s - %(message)s')

class Logger:
    def __init__(self):
        pass

    def log_critical(self, message):
        logging.critical(message)

    def log_error(self, message):
        logging.error(message)

    def log_warning(self, message):
        logging.warning(message)

    def log_info(self, message):
        logging.info(message)

    def log_debug(self, message):
        logging.debug(message)
        
    def log_exception(self, message):
        logging.exception(message)
