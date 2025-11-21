from .base_workflow_factory import WorkflowFactory

from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_maceio.pages import *
from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.infra.webdriver import get_global_webdriver
from automacao_certificados.selenium_automations.adapters import *

from automacao_certificados.config import settings

class MaceioWorkflowFactory(WorkflowFactory):
    def get_workflow(self) -> Workflow:
        driver = get_global_webdriver()
        http_client = HttpxClient()

        document_downloader = DocumentMaceioDownloader(
            download_page=DownloadPage(
                driver=driver
            )
        )
        document_persistance = CertificadoApiPersistance(
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
            document_persistance=document_persistance,
            ppe_api_persistance=ppe_api_persistance,
        )

