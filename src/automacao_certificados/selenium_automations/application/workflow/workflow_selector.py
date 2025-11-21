from automacao_certificados.selenium_automations.application.workflow.factories import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.utils import validate_cnpj

class WorkflowSelector:
    def __init__(
        self,
        municipio_api_requester: MunicipioGetterPort
    ):
        if not isinstance(municipio_api_requester, MunicipioGetterPort):
            raise ValueError("municipio_api_requester must be a MunicipioGetterPort")
        
        self.municipio_api_requester = municipio_api_requester
    
    def _get_municipio_by_cnpj(self, cnpj: str) -> MunicipioEnum:
        municipio = self.municipio_api_requester.run(cnpj)
        return municipio

    def _handle_municipal_workflow(self, cnpj: str):
        municipio = self._get_municipio_by_cnpj(cnpj)
        
        if municipio == MunicipioEnum.ARAPIRACA:
            return ArapiracaWorkflowFactory().get_workflow()
        if municipio == MunicipioEnum.MACEIO:
            return MaceioWorkflowFactory().get_workflow()
        else:
            raise ValueError("there is no workflow to download the certificate for the given municipality: {}".format(municipio))

    def _handle_fgts_workflow(self):
        return FGTSWorkflowFactory().get_workflow()

    def get_workflow(self, cnpj: str, document_type: DocumentTypeEnum):
        validate_cnpj(cnpj)
        
        if not isinstance(document_type, DocumentTypeEnum):
            raise ValueError("document_type must be a DocumentTypeEnum")

        if document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL:
            return self._handle_municipal_workflow(cnpj)
        if document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS :
            return self._handle_fgts_workflow()
        else:
            raise ValueError("there is no workflow to download the certificate for the given document type: {}".format(document_type))