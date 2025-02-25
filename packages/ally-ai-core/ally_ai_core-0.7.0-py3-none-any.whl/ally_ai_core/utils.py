import logging
import os
import sys

def get_loglevel() -> int:
    """
    returns log level 
        if LOG_LEVEL is in environment variables
    or
        'INFO'
    """
    _default_level = 'INFO'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', _default_level).upper()
    if LOG_LEVEL == '':
        LOG_LEVEL = _default_level

    return logging._nameToLevel[LOG_LEVEL]

LOG_LEVEL = get_loglevel()

def get_value_or_default(key:str, default:any, **kwargs):
    """
    returns kwargs value or default
        if key is in kwargs
    or
        default value
    """
    return kwargs[key] if key in kwargs else default


def load_test_logger(level = logging.INFO):
  test_logger = logging.getLogger()
  test_logger.setLevel(level=level)
  console_handler = logging.StreamHandler(stream=sys.stdout)
  console_handler.formatter = logging.Formatter('::> %(name)s - %(levelname)s - %(message)s')
  test_logger.handlers.clear()
  test_logger.addHandler(console_handler)