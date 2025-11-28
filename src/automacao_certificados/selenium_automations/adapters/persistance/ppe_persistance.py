from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.adapters import *

from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester

class PPEPersistance(DocumentPersistancePort):
    def __init__(self, api_requester: PPEAPIRequester):
        """
        The ppe persistance is an implementation of the document persistance port 
        that uses the ppe api to persist the document.
        """
        if not isinstance(api_requester, PPEAPIRequester):
            raise ValueError("api_requester must be a PPEAPIRequester")

        super().__init__()
        self.api_requester = api_requester

    def save(self, input: PPEPostCertificateRequest) -> DocumentPersistanceOutput:
        """
        Saves the document on database using the ppe api.

        :param input: The input of the document persistance.
        :type input: PPEPostCertificateRequest
        :return: The document persistance output.
        :rtype: DocumentPersistanceOutput
        """
        if not isinstance(input, PPEPostCertificateRequest):
            raise ValueError("input must be a PPEPostCertificateRequest")

        return DocumentPersistanceOutput(result=self.api_requester.post_certificate(input))