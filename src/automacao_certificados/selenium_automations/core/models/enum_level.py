from enum import Enum

class Level(Enum):
    """
    The severity level of the log.
    """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'
