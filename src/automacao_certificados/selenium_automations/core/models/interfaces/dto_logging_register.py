

from pydantic import BaseModel

from datetime import datetime

from enum import Enum

from typing import Optional, Any


class Level(Enum):
    """
    The severity level of the log.
    """
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'

class Status(Enum):
    """
    The status of the operation that generated the log.
    """
    SUCCESS = 'SUCCESS'
    FAILURE = 'FAILURE'

class LoggingRegisterInput(BaseModel):
    timestamp: datetime # the timestamp of the log

    facility: str # the name of the facility that generated the log
    event_name: str # the name of the event that generated the log
    level: Level # the level of the log
    message: str # the message of the log
    status: Status # the status of the log

    request_id: Optional[str] = None # to identify the API request that generated the log
    details: Optional[dict[str, Any]] = None # the details of the log
    result: Optional[Any] = None # the result of the log

    model_config = {
        "use_enum_values": True,
    }