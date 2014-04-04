import logging


def enable_console_logging():
    for identifier in ["tornado.access",
                       "tornado.application",
                       "tornado.general",
                       "vocalsalad.test"]:
        logger = logging.getLogger(identifier)
        logger.handlers = []
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
