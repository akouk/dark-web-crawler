import logging

logger = logging.getLogger("dwc_logger")
logger.setLevel(logging.INFO)
logger.propagate = False

if not logger.handlers:
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

        # Create a file handler
    fh = logging.FileHandler("log_file.txt")  # Specify the file path for the log file
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
