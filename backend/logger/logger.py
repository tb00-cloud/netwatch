import logging, sys


class LoggerFactory(object):

  _LOG = None

  @staticmethod
  def __create_logger(name, logLevel, mode):
    """
    A private method that interacts with the python
    logging module.
    """
    # set the logging format
    ch = logging.StreamHandler(stream=sys.stdout)
    jsonFormatter = logging.Formatter('{"timestamp":"%(asctime)s", "component":"' +name+ '", "level":"%(levelname)s", "module":"%(module)s","function":"%(funcName)s","message":"%(message)s"}')
    textFormatter = logging.Formatter('%(asctime)s - ' + name + ' - %(levelname)s - %(module)s - %(funcName)s - %(message)s')

    if mode != "json" and mode != "text":
      return None, "logger mode must be json or text"
    
    if mode == "json":
      ch.setFormatter(jsonFormatter)
    else:
      ch.setFormatter(textFormatter)
            
    # Initialize the class variable with logger object
    LoggerFactory._LOG = logging.getLogger(name)
    LoggerFactory._LOG.addHandler(ch)
    
    # set the logging level based on the user selection
    if logLevel == "INFO":
        LoggerFactory._LOG.setLevel(logging.INFO)
    elif logLevel == "ERROR":
        LoggerFactory._LOG.setLevel(logging.ERROR)
    elif logLevel == "DEBUG":
        LoggerFactory._LOG.setLevel(logging.DEBUG)
    return LoggerFactory._LOG, None

  @staticmethod
  def get_logger(name, logLevel, mode="json"):
    """
    A static method called by other modules to initialize logger in
    their own module. Arguments:\n
    name      - component the logger serves\n
    logLevel  - INFO, ERROR or DEBUG\n
    mode      - json or text\n
    """
    logger, err = LoggerFactory.__create_logger(name, logLevel, mode)
          
    if err is not None:
      return None, err
    
    # return the logger object
    return logger, None