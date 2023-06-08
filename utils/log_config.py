import logging

logger = logging.getLogger("dwc_logger")
logger.setLevel(logging.DEBUG)
logger.propagate = False

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # Create a file handler
    fh = logging.FileHandler("log_file.txt")  # Specify the file path for the log file
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
