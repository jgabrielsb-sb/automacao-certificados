

from pydantic import BaseModel

from datetime import datetime

from automacao_certificados.selenium_automations.core.models import (
    Status,
    Level
)

from typing import Optional, Any

class LogCreate(BaseModel):
    """
    The base model for all logs.
    """
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

class LogResponse(LogCreate):
    id: int
