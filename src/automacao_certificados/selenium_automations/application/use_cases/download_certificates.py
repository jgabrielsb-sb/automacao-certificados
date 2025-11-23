from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.exceptions import *


class DownloadCertificatesUseCase:
    def __init__(
        self, 
        ppe_api_requester: PPEAPIRequester,
        workflow_selector: WorkflowSelector
    ):
        """
        This use case is responsible for getting all the certificates
        that must be downloaded and performs it.
        """
        if not isinstance(ppe_api_requester, PPEAPIRequester):
            raise ValueError('ppe_api_requester must be a PPEAPIRequester')

        if not isinstance(workflow_selector, WorkflowSelector):
            raise ValueError('workflow_selector must be a WorkflowSelector')

        self.ppe_api_requester = ppe_api_requester
        self.workflow_selector = workflow_selector

    def _get_certificates_to_download(self) -> list[CertificateToDownload]:
        get_certificates_to_download_response = self.ppe_api_requester.get_certificates_to_download()
        return get_certificates_to_download_response

    def _download_certificate(self, certificate: CertificateToDownload) -> DownloadCertificatesUseCaseOutput:
        try:
            workflow_output = self.workflow_selector.get_workflow(
                certificate.cnpj, 
                certificate.document_type
            ).run(certificate.cnpj)
        except WorkflowSelectorException as e:
            return DownloadCertificatesUseCaseOutput(
                certificate=certificate,
                error_selection=str(e),
                workflow_output=None
            )
        
        return DownloadCertificatesUseCaseOutput(
            certificate=certificate,
            error_selection=None,
            workflow_output=workflow_output
        )

    def _download_certificates(
        self, 
        certificates_to_download: list[CertificateToDownload]
    ) -> list[DownloadCertificatesUseCaseOutput]:
        download_certificates_output = []
        
        for certificate in certificates_to_download:
            result = self._download_certificate(certificate)
            download_certificates_output.append(result)

        return download_certificates_output
            

    def run(self) -> list[DownloadCertificatesUseCaseOutput]:
        try:
            certificates_to_download = self._get_certificates_to_download()
            output = self._download_certificates(certificates_to_download)
            return output
        except Exception as e:
            raise DownloadCertificatesUseCaseException(e)




        


        

        

