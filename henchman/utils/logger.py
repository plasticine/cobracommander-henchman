import logging

def get_logger(name):
    log = logging.getLogger(name)
    log.disabled = False
    log.propagate = True
    log.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)-6s %(name)-32s %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    file_handler = logging.handlers.RotatingFileHandler('../../logs/henchman.log',
        mode='a')
    file_handler.setFormatter(formatter)
    log.addHandler(console_handler)
    log.addHandler(file_handler)
    return log
