# -*- coding: utf-8 -*-

from logging import *
import time


def get_logger(output_path="log/", level=INFO):
    logger = getLogger(__name__)
    logger.setLevel(level=level)
    output_path = output_path + str(time.time()) + '.log'
    handler = FileHandler(output_path)
    handler.setLevel(INFO)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = StreamHandler()
    console.setLevel(level)

    logger.addHandler(handler)
    logger.addHandler(console)

    return logger


def log(logger: Logger, contents,state):
    if state == DEBUG:
        logger.debug(contents)
    elif state == INFO:
        logger.info(contents)
    elif state == WARNING:
        logger.info(contents)
    elif state == ERROR:
        logger.info(contents)
    elif state == CRITICAL:
        logger.info(contents)
