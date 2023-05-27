import logging

logger = logging.getLogger('dwc_logger')
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
