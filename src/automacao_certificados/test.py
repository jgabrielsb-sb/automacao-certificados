import base64

from automacao_certificados.selenium_automations.application.workflow.factories.federal_workflow_factory import FederalWorkflowFactory
from automacao_certificados.selenium_automations.composition.container import Container
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
    # cnpj = '14876384000115'
    # #cnpj = '17086031000100'
    # # # response = api_requester.get_certificado_base64(cnpj)
    # # # print(response)

    # # # url = 'https://apiv3.directd.com.br/api/Historico?ConsultaUid=direct-f1ee8774-2448-4957-a46e-a1f74ea2dd02&Extensao=pdf'

    # # # response = httpx_client.get(url)
    # # # base64_pdf = base64.b64encode(response.content).decode("utf-8")
    # # # print(base64_pdf)
    # # workflow = FederalWorkflowFactory().get_workflow()
    # # output = workflow.run(cnpj)
    # # print(output)

    # receita_api_getter = container.adapter_factory.create_receita_api_requester()
    # company = receita_api_getter.get_company(cnpj)
    # print(company)
    from datetime import datetime
    certificates_to_download = [
        CertificateToDownload(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
        )
    ]
    logging_register = container.service_factory.create_certificado_logging_register_service()
    logging_register.register_download_certificate_result(
        input=RegisterDownloadCertificateResult(
            certificate_to_download=certificates_to_download[0],
            download_certificate_result=DownloadCertificateResult(
                certificate=certificates_to_download[0],
                error_selection="error",
                workflow_output=WorkflowOutput(
                    download_output_result=StepResult(
                        sucess=True,
                    ),
                    persistance_output_result=StepResult(
                        sucess=True
                    ),
                    ppe_output_result=StepResult(
                        sucess=True
                    )
                )
            ),
            download_datetime=datetime.now()
        )
    )
    



    