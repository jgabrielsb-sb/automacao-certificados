from pydantic import BaseModel

from typing import Any

from automacao_certificados.selenium_automations.core.models.enum_status import Status

class StepResult(BaseModel):
    sucess: bool
    error_message: str | None = None
    output: Any | None = None


class WorkflowOutput(BaseModel):
    download_output_result: StepResult | None = None
    persistance_output_result: StepResult | None = None
    ppe_output_result: StepResult | None = None

    @property
    def sucess(self):
        if not self.download_output_result.sucess:
            return Status.FAILURE
        elif (not self.persistance_output_result.sucess) or (not self.ppe_output_result.sucess):
            return Status.PARTIAL
        else:
            return Status.SUCCESS
