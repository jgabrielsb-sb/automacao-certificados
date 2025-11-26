from .base_workflow_factory import WorkflowFactory

from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.adapters import *

from automacao_certificados.config import settings

from automacao_certificados.selenium_automations.infra.api_requester import (
    AlagoasAPIRequester,
    CertificadoAPIRequester,
    PPEAPIRequester
)


class AlagoasWorkflowFactory(WorkflowFactory):
    def get_workflow(self) -> Workflow:
        
        http_client = HttpxClient()
        document_downloader = DocumentAlagoasDownloader(
            api_requester=AlagoasAPIRequester(
                http=http_client
            )
        )
        certificado_api_persistance = CertificadoApiPersistance(
            api_requester=CertificadoAPIRequester(
                base_url=settings.base_certificado_api_url,
                http=http_client
            )
        )
        ppe_api_persistance = PPEPersistance(
            api_requester=PPEAPIRequester(
                http=http_client,
                api_key=settings.ppe_api_key
            )
        )
        return Workflow(
            document_downloader=document_downloader,
            certificado_api_persistance=certificado_api_persistance,
            ppe_api_persistance=ppe_api_persistance,
        )