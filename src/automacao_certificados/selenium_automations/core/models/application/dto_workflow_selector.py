
from pydantic import BaseModel

class WorkflowSelectorOutput(BaseModel):
    sucess: bool
    error_message: str | None = None
