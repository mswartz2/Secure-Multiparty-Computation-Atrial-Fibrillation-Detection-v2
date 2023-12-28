import logging
import os


# DESCRIPTION:  Setup the logging
#
# INPUTS:   level - the level of messages to be logged
#           output_filepath - the file path for the log file to be stored
#           logging_type - the output of the logging messages
# RETURNS:  -
# NOTES: logging_type can take the following values: 1 -> stdout, 2 -> file, 3 -> both
#        level can take the following values: 0 -> NOTSET, 10 -> DEBUG, 20 -> INFO, 30 -> WARNING, 40 -> ERROR, 50 -> CRITICAL
def setupLogging(level, output_filepath, logging_type):

    logger = logging.getLogger()
    formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
    logger.setLevel(level)
    if logging_type == 0:
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    elif logging_type == 1:
        directory = os.path.dirname(output_filepath)
        os.makedirs(directory, exist_ok=True)
        handler = logging.FileHandler(filename=output_filepath)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    elif logging_type == 2:
        handler_stdout = logging.StreamHandler()
        directory = os.path.dirname(output_filepath)
        os.makedirs(directory, exist_ok=True)
        handler_file = logging.FileHandler(filename=output_filepath)
        handler_stdout.setFormatter(formatter)
        handler_file.setFormatter(formatter)
        logger.addHandler(handler_stdout)
        logger.addHandler(handler_file)


def convertLoggingLevel(level):
    if level is 0:
        return logging.NOTSET
    elif level is 10:
        return logging.DEBUG
    elif level is 20:
        return logging.INFO
    elif level is 30:
        return logging.WARNING
    elif level is 40:
        return logging.ERROR
    elif level is 50:
        return logging.CRITICAL
