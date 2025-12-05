
from enum import Enum

class Status(Enum):
    """
    The status of the operation that generated the log.
    """
    SUCCESS = 'SUCCESS'
    PARTIAL = 'PARTIAL'
    FAILURE = 'FAILURE'