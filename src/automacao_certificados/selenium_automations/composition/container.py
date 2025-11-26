"""
Main dependency injection container.

This is the composition root where all dependencies are wired together.
It provides a single entry point for getting configured application components.
"""

from .infrastructure import InfrastructureProvider
from .adapters import AdapterFactory
from .use_cases import UseCaseFactory


class Container:
    """
    Main dependency injection container.
    
    This container creates and manages all dependencies in the application.
    It follows the composition root pattern, centralizing object creation.
    
    Usage:
        container = Container()
        use_case = container.get_download_certificates_use_case()
    """
    
    def __init__(self):
        """Initialize the container and wire all dependencies."""
        self.infrastructure = InfrastructureProvider()
        self.adapter_factory = AdapterFactory(self.infrastructure)
        self.use_case_factory = UseCaseFactory(self.adapter_factory)
    
    def get_download_certificates_use_case(self):
        """
        Get configured download certificates use case.
        
        Returns:
            DownloadCertificatesUseCase instance with all dependencies wired.
        """
        return self.use_case_factory.create_download_certificates_use_case()

