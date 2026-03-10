from .base_workflow_factory import WorkflowFactory

from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.infra.webdriver import get_global_webdriver
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.infra.api_requester import (
    AlagoasAPIRequester,
    CertificadoAPIRequester,
    PPEAPIRequester,
    DirectDataAPIRequester
)

from automacao_certificados.config import settings

class FederalWorkflowFactory(WorkflowFactory):
    def get_workflow(self) -> Workflow:
        #driver = get_global_webdriver()
        http_client = HttpxClient()

        ppe_api_requester = PPEAPIRequester(
            http=http_client,
            api_key=settings.ppe_api_key,
            base_url=settings.base_ppe_api_url
        )

        document_downloader = DocumentFederalDownloader(
            api_requester=DirectDataAPIRequester(
                http=http_client,
                token=settings.direct_data_api_key,
                base_url=settings.base_direct_data_api_url
            ),
            ppe_api_requester=ppe_api_requester
        )
        
        certificado_api_persistance = CertificadoApiPersistance(
            api_requester=CertificadoAPIRequester(
                base_url=settings.base_certificado_api_url,
                http=http_client
            )
        )

        ppe_api_persistance = PPEPersistance(
            api_requester=ppe_api_requester
        )

        return Workflow(
            document_downloader=document_downloader,
            certificado_api_persistance=certificado_api_persistance,
            ppe_api_persistance=ppe_api_persistance,
        )

