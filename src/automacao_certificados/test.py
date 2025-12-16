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
ppe_api_requester = container.adapter_factory.create_ppe_api_requester()
direct_data_api_requester = container.adapter_factory.create_direct_data_api_requester()

if __name__ == "__main__":
    #response = ppe_api_requester.block_certificate(cnpj="57142978000105", document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL)
    response = direct_data_api_requester.get_certificado_url(cnpj="21798960000119")
    print(response)


    