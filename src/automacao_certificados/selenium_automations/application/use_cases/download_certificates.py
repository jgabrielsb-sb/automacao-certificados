

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.exceptions import *

from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester
from automacao_certificados.selenium_automations.application.services import LoggingRegisterService

class DownloadCertificatesUseCase:
    def __init__(
        self, 
        ppe_api_requester: PPEAPIRequester,
        workflow_selector: WorkflowSelector,
        logging_register_service: LoggingRegisterService
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

        if not isinstance(logging_register_service, LoggingRegisterService):
            raise ValueError('logging_register_service must be a LoggingRegisterService')

        self.ppe_api_requester = ppe_api_requester
        self.workflow_selector = workflow_selector
        self.logging_register_service = logging_register_service

    def _register_download_certificates_cron_execution(
        self, 
        certificates_to_download: list[CertificateToDownload]
    ) -> None:
        """
        Registers the execution of the download certificates cron.
        """
        if not isinstance(certificates_to_download, list):
            raise ValueError('certificates_to_download must be a list')

        if not all(isinstance(certificate, CertificateToDownload) for certificate in certificates_to_download):
            raise ValueError('all elements of certificates_to_download must be CertificateToDownload')

        try:
            self.logging_register_service.register_download_certificates_cron_execution(
                input=RegisterDownloadCertificatesCronExecution(
                    certificates_to_download=certificates_to_download,
                    cron_datetime=datetime.now()
                )
            )
        except LoggingRegisterServiceException as e:
            print(f"Error registering download certificates cron execution: {e}")

    def _register_download_certificate_result(
        self, 
        certificate_to_download: CertificateToDownload,
        download_certificate_result: DownloadCertificateResult
    ) -> None:
        """
        Registers the result of the download certificate.
        """
        try:
            self.logging_register_service.register_download_certificate_result(
                input=RegisterDownloadCertificateResult(
                    certificate_to_download=certificate_to_download,
                    download_certificate_result=download_certificate_result,
                    download_datetime=datetime.now()
                )
            )
        except LoggingRegisterServiceException as e:
            print(f"Error registering download certificate result: {e}")

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
        if not isinstance(certificate, CertificateToDownload):
            raise ValueError('certificate must be a CertificateToDownload')
        
        # Get municipality for municipal certificates
        municipio = None
        try:
            municipio = self.workflow_selector.get_municipio_for_certificate(
                certificate.cnpj,
                certificate.document_type
            )
        except Exception:
            # If we can't get municipality, continue without it
            pass
        
        try:
            workflow_output = self.workflow_selector.get_workflow(
                certificate.cnpj, 
                certificate.document_type
            ).run(certificate.cnpj)
        except WorkflowSelectorException as e:
            return DownloadCertificateResult(
                certificate=certificate,
                error_selection=str(e),
                workflow_output=WorkflowOutput(),
                municipio=municipio
            )
        
        return DownloadCertificateResult(
            certificate=certificate,
            error_selection=None,
            workflow_output=workflow_output,
            municipio=municipio
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
        if not isinstance(certificates_to_download, list):
            raise ValueError('certificates_to_download must be a list')

        if not all(isinstance(certificate, CertificateToDownload) for certificate in certificates_to_download):
            raise ValueError('all elements of certificates_to_download must be CertificateToDownload')

        download_certificates_output = []
        
        for certificate in certificates_to_download:
            result = self._download_certificate(certificate)
            self._register_download_certificate_result(certificate, result)
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
        try:
            certificates_to_download = self._get_certificates_to_download()
            self._register_download_certificates_cron_execution(certificates_to_download)
            output = self._download_certificates(certificates_to_download)
            return output
        except Exception as e:
            raise DownloadCertificatesUseCaseException(e)




        


        

        

