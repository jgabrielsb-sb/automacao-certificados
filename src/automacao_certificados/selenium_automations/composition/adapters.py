"""
Adapter factory for creating adapter instances.

This module creates adapter instances that implement the ports (interfaces)
defined in the core layer.
"""

from automacao_certificados.selenium_automations.adapters import (
    ReceitaAPIMunicipioGetter,
)
from automacao_certificados.selenium_automations.adapters.email import SMTPEmailSender
from automacao_certificados.selenium_automations.adapters.estado_getter.receita_api_getter import ReceitaAPIEstadoGetter
from automacao_certificados.selenium_automations.adapters.logging_register.certificado_api import CertificadoAPILoggingRegister
from automacao_certificados.selenium_automations.core.models.infra.dto_email import EmailConfig
from automacao_certificados.selenium_automations.infra.api_requester import (
    PPEAPIRequester,
    CertificadoAPIRequester,
    ReceitaAPIRequester,
)
from automacao_certificados.config import settings
from automacao_certificados.selenium_automations.infra.api_requester.direct_data_api_requester import DirectDataAPIRequester
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
            http=self.infrastructure.http_client,
            base_url=settings.nota_facil_base_url
        )
    
    def create_direct_data_api_requester(self) -> DirectDataAPIRequester:
        return DirectDataAPIRequester(
            http=self.infrastructure.http_client,
            token=settings.direct_data_api_key
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

    def create_receita_api_estado_getter(self) -> ReceitaAPIEstadoGetter:
        """
        Create Receita API estado getter adapter

        Returns:
            Configured ReceitaAPIEstadoGetter instance
        """
        return ReceitaAPIEstadoGetter(
            api_requester=self.create_receita_api_requester()
        )


    def create_smtp_email_sender(self) -> SMTPEmailSender:
        """
        Create a SMTPEmailSender adapter

        :rtype: None
        """
        return SMTPEmailSender(
            email_config=EmailConfig(
                email_host=settings.email_host,
                email_port=settings.email_port,
                is_tls=settings.is_tls,
                email_host_user=settings.email_host_user,
                email_host_password=settings.email_host_password,
            )
        )
    
    def create_certificado_api_logging_register(self) -> CertificadoAPILoggingRegister:
        """
        Create Certificado API Logging Register

        rtype: CertificadoAPILoggingRegister
        """
        return CertificadoAPILoggingRegister(
            api_requester=self.create_certificado_api_requester()
        )
