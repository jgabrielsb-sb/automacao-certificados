from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import (
    CertificateToDownload, 
    WorkflowOutput,
)

class DownloadCertificateResult(BaseModel):
    certificate: CertificateToDownload
    error_selection: str | None = None
    workflow_output: WorkflowOutput

class DownloadCertificatesUseCaseOutput(BaseModel):
    output: list[DownloadCertificateResult]