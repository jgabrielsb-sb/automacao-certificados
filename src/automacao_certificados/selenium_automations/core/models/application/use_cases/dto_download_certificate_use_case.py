from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import (
    CertificateToDownload, 
    WorkflowOutput,
)

class DownloadCertificatesUseCaseOutput(BaseModel):
    certificate: CertificateToDownload
    error_selection: str | None = None
    workflow_output: WorkflowOutput