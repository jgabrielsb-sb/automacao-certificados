
from pydantic import BaseModel

from datetime import datetime

from automacao_certificados.selenium_automations.core.models.adapters.api_requester.dto_ppe_api import CertificateToDownload
from automacao_certificados.selenium_automations.core.models.application.use_cases.dto_download_certificate_use_case import DownloadCertificateResult



class RegisterDownloadCertificatesCronExecution(BaseModel):
    certificates_to_download: list[CertificateToDownload]
    cron_datetime: datetime

class RegisterDownloadCertificateResult(BaseModel):
    certificate_to_download: CertificateToDownload
    download_certificate_result: DownloadCertificateResult
    download_datetime: datetime






