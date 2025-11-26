from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *

from typing import Callable, Any

class Workflow:
    def __init__(
        self,
        document_downloader: DocumentDownloaderPort,
        certificado_api_persistance: CertificadoApiPersistance,
        ppe_api_persistance: PPEPersistance,
    ):
        """
        The workflow is responsible for performing the download of the certificate and persisting 
        the data in the certificado api and ppe api.
        """
        if not isinstance(document_downloader, DocumentDownloaderPort):
            raise ValueError('document_downloader must be a DocumentDownloaderPort')

        if not isinstance(certificado_api_persistance, CertificadoApiPersistance):
            raise ValueError('certificado_api_persistance must be a CertificadoApiPersistance')

        if not isinstance(ppe_api_persistance, PPEPersistance):
            raise ValueError('ppe_api_persistance must be a PPEPersistance')

        self.document_downloader = document_downloader
        self.certificado_api_persistance = certificado_api_persistance
        self.ppe_api_persistance = ppe_api_persistance

    def perform_download(self, cnpj):
        """
        Performs the download of the certificate by running the document downloader.

        :param cnpj: The cnpj of the company to download the certificate.
        :type cnpj: str
        :return: The step result.
        :rtype: StepResult
        """
        try:
            output = self.document_downloader.run(cnpj)
            sucess = True
            error_message = None
        except DocumentDownloaderException as e:
            output = None
            sucess = False
            error_message = str(e)
            
        return StepResult(sucess=sucess,error_message=error_message,output=output)
        
    def persist_data_in_certificado_api(
        self, 
        certificado_api_persistance_input: DocumentPersistanceInput
    ) -> StepResult:
        """
        Persists the data in the certificado api by running the certificado api persistance.

        :param certificado_api_persistance_input: The input of the certificado api persistance.
        :type certificado_api_persistance_input: DocumentPersistanceInput
        :return: The step result.
        :rtype: StepResult
        """
        try:
            output = self.certificado_api_persistance.run(certificado_api_persistance_input)
            sucess = True
            error_message = None
        except DocumentPersistanceException as e:
            output = None
            sucess = False
            error_message = str(e)
            
        return StepResult(sucess=sucess, error_message=error_message, output=output)

    def persist_data_in_ppe_api(
        self, 
        ppe_api_persistance_input: PPEPostCertificateRequest
    ) -> StepResult:
        """
        Persists the data in the ppe api by running the ppe api persistance.

        :param ppe_api_persistance_input: The input of the ppe api persistance.
        :type ppe_api_persistance_input: PPEPostCertificateRequest
        :return: The step result.
        :rtype: StepResult
        """
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
        """
        Runs the workflow by performing the download of the certificate and persisting the data in the certificado api and ppe api.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The workflow output.
        :rtype: WorkflowOutput
        """
        document_downloader_output = self.perform_download(
            DocumentDownloaderInput(
                cnpj=cnpj,
            )   
        )
        certificado_api_persistance_output = None
        ppe_api_persistance_output = None

        if document_downloader_output.sucess:
            certificado_api_persistance_output = self.persist_data_in_certificado_api(
                DocumentPersistanceInput(
                    document_extracted=document_downloader_output.output.document_extracted,
                    base64_pdf=document_downloader_output.output.base64_pdf,
                )
            )

            ppe_api_persistance_output = self.persist_data_in_ppe_api(
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
            persistance_output_result=certificado_api_persistance_output,
            ppe_output_result=ppe_api_persistance_output,
        )


        