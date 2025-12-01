"""
Use case factory for creating use case instances.

This module creates use cases and wires them with their dependencies.
"""

from automacao_certificados.selenium_automations.application.use_cases import (
    DownloadCertificatesUseCase,
    SendDownloadCertificatesReportViaEmailUseCase
)
from automacao_certificados.selenium_automations.application.use_cases.email_use_cases import SendApplicationBrokeReportViaEmailUseCase
from automacao_certificados.selenium_automations.application.workflow.workflow_selector import (
    WorkflowSelector
)
from .adapters import AdapterFactory


class UseCaseFactory:
    """
    Factory for creating use case instances.
    
    Use cases orchestrate the application logic and coordinate between
    different adapters and workflows.
    """
    
    def __init__(self, adapter_factory: AdapterFactory):
        """
        Initialize use case factory.
        
        Args:
            adapter_factory: Factory for creating adapters.
        """
        self.adapter_factory = adapter_factory
    
    def create_download_certificates_use_case(self) -> DownloadCertificatesUseCase:
        """
        Create download certificates use case.
        
        Returns:
            Configured DownloadCertificatesUseCase instance with all dependencies.
        """
        return DownloadCertificatesUseCase(
            ppe_api_requester=self.adapter_factory.create_ppe_api_requester(),
            workflow_selector=WorkflowSelector(
                municipio_api_requester=self.adapter_factory.create_receita_api_municipio_getter()
            )
        )
    
    def create_send_download_certificates_report_via_email_use_case(self) -> SendDownloadCertificatesReportViaEmailUseCase:
        """
        Create send download certificates report via email use case.
        
        Returns:
            Configured SendDownloadCertificatesReportViaEmailUseCase instance with all dependencies.
        """
        return SendDownloadCertificatesReportViaEmailUseCase(
            email_sender=self.adapter_factory.create_smtp_email_sender()
        )

    def create_send_application_broke_report_via_email_use_case(self) -> SendApplicationBrokeReportViaEmailUseCase:
        """
        Create send application broke report via email use case.

        :return: the use case itself
        :rtype: SendApplicationBrokeReportViaEmailUseCase
        """
        return SendApplicationBrokeReportViaEmailUseCase(
            email_sender=self.adapter_factory.create_smtp_email_sender()
        )

