from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import (
    CertificateToDownload, 
    WorkflowOutput
)
from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import WorkflowOutput

class DownloadCertificateResult(BaseModel):
    certificate: CertificateToDownload
    error_selection: str | None = None
    workflow_output: WorkflowOutput

class DownloadCertificatesUseCaseOutput(BaseModel):
    output: list[DownloadCertificateResult]