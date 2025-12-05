"""
Use case factory for creating use case instances.

This module creates use cases and wires them with their dependencies.
"""

from automacao_certificados.selenium_automations.application.use_cases.email_use_cases import SendApplicationBrokeReportViaEmailUseCase
from automacao_certificados.selenium_automations.application.workflow.workflow_selector import (
    WorkflowSelector
)

from automacao_certificados.selenium_automations.application.services import (
    LoggingRegisterService
)

from .adapters import AdapterFactory


class ServiceFactory:
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
    
    def create_certificado_logging_register_service(self) -> LoggingRegisterService:
        """
        Create logging register service.
        
        Returns:
            Configured LoggingRegisterService instance with all dependencies.
        """
        return LoggingRegisterService(
            logging_register=self.adapter_factory.create_certificado_api_logging_register()
        )


