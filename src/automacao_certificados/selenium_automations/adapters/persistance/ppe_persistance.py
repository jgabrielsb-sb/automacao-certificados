from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.adapters import *

from automacao_certificados.selenium_automations.infra.api_requester import PPEAPIRequester

class PPEPersistance(DocumentPersistancePort):
    def __init__(self, api_requester: PPEAPIRequester):
        self.api_requester = api_requester

    def _save(self, input: DocumentPersistanceInput) -> DocumentPersistanceOutput:
        return DocumentPersistanceOutput(result=self.api_requester.post_certificate(input))