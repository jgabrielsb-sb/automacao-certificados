"""
Adapter factory for creating adapter instances.

This module creates adapter instances that implement the ports (interfaces)
defined in the core layer.
"""

from automacao_certificados.selenium_automations.adapters import (
    ReceitaAPIMunicipioGetter,
)
from automacao_certificados.selenium_automations.infra.api_requester import (
    PPEAPIRequester,
    CertificadoAPIRequester,
    ReceitaAPIRequester,
)
from automacao_certificados.config import settings
from .infrastructure import InfrastructureProvider


class AdapterFactory:
    """
    Factory for creating adapter instances.
    
    Adapters implement the ports (interfaces) and connect the application
    to external systems.
    """
    
    def __init__(self, infrastructure: InfrastructureProvider):
        """
        Initialize adapter factory.
        
        Args:
            infrastructure: Provider for infrastructure objects.
        """
        self.infrastructure = infrastructure
    
    def create_ppe_api_requester(self) -> PPEAPIRequester:
        """
        Create PPE API requester adapter.
        
        Returns:
            Configured PPEAPIRequester instance.
        """
        return PPEAPIRequester(
            http=self.infrastructure.http_client,
            api_key=settings.ppe_api_key
        )
    
    def create_certificado_api_requester(self) -> CertificadoAPIRequester:
        """
        Create Certificado API requester adapter.
        
        Returns:
            Configured CertificadoAPIRequester instance.
        """
        return CertificadoAPIRequester(
            base_url=settings.base_certificado_api_url,
            http=self.infrastructure.http_client
        )
    
    def create_receita_api_requester(self) -> ReceitaAPIRequester:
        """
        Create Receita API requester adapter.
        
        Returns:
            Configured ReceitaAPIRequester instance.
        """
        return ReceitaAPIRequester(
            http=self.infrastructure.http_client
        )
    
    def create_receita_api_municipio_getter(self) -> ReceitaAPIMunicipioGetter:
        """
        Create Receita API municipio getter adapter.
        
        Returns:
            Configured ReceitaAPIMunicipioGetter instance.
        """
        return ReceitaAPIMunicipioGetter(
            api_requester=self.create_receita_api_requester()
        )

