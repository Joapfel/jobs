import logging
from time import strftime


def init_logger(path):
    timestamp_format = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                  datefmt=timestamp_format)

    # stream to console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)

    # logg to file
    file_handler = logging.FileHandler(f'{path}-{strftime(timestamp_format)}.log')
    file_handler.setFormatter(formatter)

    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger
