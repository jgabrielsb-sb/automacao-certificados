from pydantic import BaseModel

from typing import Any

class StepResult(BaseModel):
    sucess: bool
    error_message: str | None = None
    output: Any | None = None


class WorkflowOutput(BaseModel):
    download_output_result: StepResult | None = None
    persistance_output_result: StepResult | None = None
    ppe_output_result: StepResult | None = None

    @property
    def sucess(self) ->  bool:
        return all(step.sucess for step in [self.download_output_result, self.persistance_output_result, self.ppe_output_result] if step is not None)
