"""
Infrastructure provider for shared infrastructure objects.

This module provides singleton or shared instances of infrastructure
components like HTTP clients, webdriver, and external service clients.
"""

from automacao_certificados.selenium_automations.adapters.http import HttpxClient
from automacao_certificados.selenium_automations.infra.webdriver import get_global_webdriver
from automacao_certificados.config import settings
from groq import Groq


class InfrastructureProvider:
    """
    Provides infrastructure objects (singletons or shared instances).
    
    This class manages the lifecycle of infrastructure components that
    should be shared across the application.
    """
    
    def __init__(self):
        self._http_client = None
        self._webdriver = None
        self._groq_client = None
    
    @property
    def http_client(self) -> HttpxClient:
        """
        Get or create HTTP client (singleton).
        
        Returns:
            Shared instance of HttpxClient.
        """
        if self._http_client is None:
            self._http_client = HttpxClient()
        return self._http_client
    
    @property
    def webdriver(self):
        """
        Get or create webdriver instance.
        
        Returns:
            Shared webdriver instance.
        """
        if self._webdriver is None:
            self._webdriver = get_global_webdriver()
        return self._webdriver
    
    @property
    def groq_client(self) -> Groq:
        """
        Get or create Groq client (singleton).
        
        Returns:
            Shared instance of Groq client configured with API key.
        """
        if self._groq_client is None:
            self._groq_client = Groq(api_key=settings.groq_api_key)
        return self._groq_client

