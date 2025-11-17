from automacao_certificados.selenium_automations.application.workflows.certificado_alagoas_workflow import CertificadoAlagoasWorkflow
from automacao_certificados.selenium_automations.adapters.api_requester.alagoas_api_requester import AlagoasAPIRequester
from automacao_certificados.selenium_automations.adapters.http import HttpxClient

from automacao_certificados.selenium_automations.core.models import dto_document

def download_certificado_alagoas(
    cnpj: str
) -> tuple[dto_document.DocumentExtracted, str]:
    document_extracted, base64_pdf = CertificadoAlagoasWorkflow(
        api_requester=AlagoasAPIRequester(
            http=HttpxClient()
        )
    ).run(cnpj=cnpj)
    
    return document_extracted, base64_pdf