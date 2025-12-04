

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.exceptions import *

from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester

class DownloadCertificatesUseCase:
    def __init__(
        self, 
        ppe_api_requester: PPEAPIRequester,
        workflow_selector: WorkflowSelector
    ):
        """
        This use case is responsible for getting:
        * all the certificates that must be downloaded;
        * use the workflow selector to get the correspondent workflow for each certificate;
        * download the certificate;
        
        It returns a list of DownloadCertificateResult objects.
        """
        if not isinstance(ppe_api_requester, PPEAPIRequester):
            raise ValueError('ppe_api_requester must be a PPEAPIRequester')

        if not isinstance(workflow_selector, WorkflowSelector):
            raise ValueError('workflow_selector must be a WorkflowSelector')

        self.ppe_api_requester = ppe_api_requester
        self.workflow_selector = workflow_selector

    def _get_certificates_to_download(self) -> list[CertificateToDownload]:
        """
        Returns the list of certificates that must be downloaded.
        
        :return: the list of certificates that must be downloaded.
        :rtype: list[CertificateToDownload]
        """
        get_certificates_to_download_response = self.ppe_api_requester.get_certificates_to_download()
        return get_certificates_to_download_response

    def _download_certificate(self, certificate: CertificateToDownload) -> DownloadCertificateResult:
        """
        Given a certificate, it uses the workflow selector to get the correspondent
        workflow and runs it to download the certificate.

        :param certificate: the certificate to download.
        :type certificate: CertificateToDownload
        :return: the output of the download certificate use case.
        :rtype: DownloadCertificateResult
        """
        try:
            workflow_output = self.workflow_selector.get_workflow(
                certificate.cnpj, 
                certificate.document_type
            ).run(certificate.cnpj)
        except WorkflowSelectorException as e:
            return DownloadCertificateResult(
                certificate=certificate,
                error_selection=str(e),
                workflow_output=WorkflowOutput()
            )
        
        return DownloadCertificateResult(
            certificate=certificate,
            error_selection=None,
            workflow_output=workflow_output
        )

    def _download_certificates(
        self, 
        certificates_to_download: list[CertificateToDownload]
    ) -> DownloadCertificatesUseCaseOutput:
        """
        Given a list of certificates, it downloads each one of them using the _download_certificate method.
        
        :param certificates_to_download: the list of certificates to download.
        :type certificates_to_download: list[CertificateToDownload]
        :return: the list of outputs of the download certificate use case.
        :rtype: list[DownloadCertificateResult]
        """
        download_certificates_output = []
        
        for certificate in certificates_to_download:
            result = self._download_certificate(certificate)
            print(result)
            download_certificates_output.append(result)

        return DownloadCertificatesUseCaseOutput(
            output=download_certificates_output
        )
            

    def run(self) -> DownloadCertificatesUseCaseOutput:
        """
        This method is the entry point of the use case.
        It gets the certificates to download, downloads them and returns the list of outputs.
        
        :return: the list of outputs of the download certificate use case.
        :rtype: list[DownloadCertificateResult]
        """
        print('ta aqui!')
        try:
            certificates_to_download = self._get_certificates_to_download()
            output = self._download_certificates(certificates_to_download)
            return output
        except Exception as e:
            raise DownloadCertificatesUseCaseException(e)




        


        

        

