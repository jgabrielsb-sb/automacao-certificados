import base64

from automacao_certificados.selenium_automations.application.workflow.factories.federal_workflow_factory import FederalWorkflowFactory
from automacao_certificados.selenium_automations.composition.container import Container
from automacao_certificados.selenium_automations.core.models import DocumentFilter
from automacao_certificados.selenium_automations.core.models.adapters.api_requester.dto_ppe_api import CertificateToDownload, DocumentTypeEnum
from automacao_certificados.selenium_automations.core.models.application.services.dto_logging_register_service import RegisterDownloadCertificateResult, RegisterDownloadCertificatesCronExecution
from automacao_certificados.selenium_automations.core.models.application.use_cases.dto_download_certificate_use_case import DownloadCertificateResult
from automacao_certificados.selenium_automations.core.models.interfaces.dto_logging_register import LoggingRegisterInput
from automacao_certificados.selenium_automations.core.models import Level, Status
from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import StepResult, WorkflowOutput

container = Container()
api_requester = container.adapter_factory.create_direct_data_api_requester()
httpx_client = container.infrastructure.http_client

if __name__ == "__main__":
    certificado_api_requester = container.adapter_factory.create_certificado_api_requester()
    documents = certificado_api_requester.get_document(
        DocumentFilter(
            identifier="Tribut",
        )
    )
    base64_pdf = base64.b64decode(documents[0].base64_pdf.encode("utf-8"))
    with open("document.pdf", "wb") as f:
        f.write(base64_pdf)



    