from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *

from typing import Callable, Any

class Workflow:
    def __init__(
        self,
        document_downloader: DocumentDownloaderPort,
        document_persistance: DocumentPersistancePort,
        ppe_api_persistance: DocumentPersistancePort,
    ):
        if not isinstance(document_downloader, DocumentDownloaderPort):
            raise ValueError('document_downloader must be a DocumentDownloaderPort')

        if not isinstance(document_persistance, DocumentPersistancePort):
            raise ValueError('document_persistance must be a DocumentPersistancePort')

        if not isinstance(ppe_api_persistance, DocumentPersistancePort):
            raise ValueError('ppe_api_persistance must be a DocumentPersistancePort')

        self.document_downloader = document_downloader
        self.document_persistance = document_persistance
        self.ppe_api_persistance = ppe_api_persistance

    def perform_download(self, cnpj):
        
        try:
            output = self.document_downloader.run(cnpj)
            sucess = True
            error_message = None
        except DocumentDownloaderException as e:
            output = None
            sucess = False
            error_message = str(e)
            
        return StepResult(sucess=sucess,error_message=error_message,output=output)
        
    def persist_data(self, document_persistance_input: DocumentPersistanceInput):
        try:
            output = self.document_persistance.run(document_persistance_input)
            sucess = True
            error_message = None
        except DocumentPersistanceException as e:
            output = None
            sucess = False
            error_message = str(e)
            
        return StepResult(sucess=sucess, error_message=error_message, output=output)

    def persist_data_in_ppe(self, ppe_api_persistance_input: PPEPostCertificateRequest):
        try:
            output = self.ppe_api_persistance.run(ppe_api_persistance_input)
            sucess = True
            error_message = None
        except DocumentPersistanceException as e:
            output = None
            sucess = False
            error_message = str(e)
            
        return StepResult(sucess=sucess, error_message=error_message, output=output)

    def run(self, cnpj) -> WorkflowOutput:
        document_downloader_output = self.perform_download(
            DocumentDownloaderInput(
                cnpj=cnpj,
            )   
        )
        document_persistance_output = None
        ppe_api_requester_output = None

        if document_downloader_output.sucess:
            document_persistance_output = self.persist_data(
                DocumentPersistanceInput(
                    document_extracted=document_downloader_output.output.document_extracted,
                    base64_pdf=document_downloader_output.output.base64_pdf,
                )
            )

            ppe_api_requester_output = self.persist_data_in_ppe(
                PPEPostCertificateRequest(
                    document=cnpj,
                    certificate=DocumentTypeEnum(document_downloader_output.output.document_extracted.document_type),
                    number=document_downloader_output.output.document_extracted.identifier,
                    validity=document_downloader_output.output.document_extracted.expiration_date,
                    pdf=document_downloader_output.output.base64_pdf,
                )
            )
        

        return WorkflowOutput(
            download_output_result=document_downloader_output,
            persistance_output_result=document_persistance_output,
            ppe_output_result=ppe_api_requester_output,
        )


        