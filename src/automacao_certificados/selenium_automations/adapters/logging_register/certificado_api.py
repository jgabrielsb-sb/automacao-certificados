
from automacao_certificados.selenium_automations.core.interfaces import LoggingRegisterPort
from automacao_certificados.selenium_automations.core.models.dto_log import LogCreate
from automacao_certificados.selenium_automations.core.models.interfaces.dto_logging_register import LoggingRegisterInput
from automacao_certificados.selenium_automations.infra import CertificadoAPIRequester

class CertificadoAPILoggingRegister(LoggingRegisterPort):
    def __init__(
        self,
        api_requester: CertificadoAPIRequester
    ):
        if not isinstance(api_requester, CertificadoAPIRequester):
            raise ValueError('api_requester must be a CertificadoAPIRequester')

        self.api_requester = api_requester

    def register(self, input: LoggingRegisterInput):
        log_create = LogCreate(**input.model_dump(mode="json"))
        log_response = self.api_requester.register_log(log_create)
        return log_response

    

        
