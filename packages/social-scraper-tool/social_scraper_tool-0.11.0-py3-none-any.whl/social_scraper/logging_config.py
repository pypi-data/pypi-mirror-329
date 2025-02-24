import logging

# LOGGING CONFIG
logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(process)d - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - "
                              "%(message)s",
                              datefmt="%d-%b-%y %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)
