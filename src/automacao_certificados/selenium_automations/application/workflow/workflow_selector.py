from automacao_certificados.selenium_automations.application.workflow.factories import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.utils import validate_cnpj
from automacao_certificados.selenium_automations.core.exceptions import *

class WorkflowSelector:
    def __init__(
        self,
        municipio_api_requester: MunicipioGetterPort
    ):
        """
        The workflow selector is responsible for selecting the correct workflow based on the cnpj and document type.

        """
        if not isinstance(municipio_api_requester, MunicipioGetterPort):
            raise ValueError("municipio_api_requester must be a MunicipioGetterPort")
        
        self.municipio_api_requester = municipio_api_requester
    
    def _get_municipio_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the municipality by cnpj using the municipio api requester.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The municipality name.
        :rtype: str
        """
        municipio = self.municipio_api_requester.run(cnpj)
        return municipio

    def _handle_municipal_workflow(self, cnpj: str):
        """
        Handles the case where the document type is a municipal certificate by 
        selecting the correct workflow based on the municipality.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The workflow.
        :rtype: Workflow
        :raises MunicipioNotSupportedException: If the municipality is not supported.
        """
        municipio = self._get_municipio_by_cnpj(cnpj)
        
        if municipio == "ARAPIRACA":
            return ArapiracaWorkflowFactory().get_workflow()
        if municipio == "MACEIO":
            return MaceioWorkflowFactory().get_workflow()
        else:
            raise MunicipioNotSupportedException("there is no workflow to download the certificate for the given municipality: {}".format(municipio))

    def _handle_fgts_workflow(self):
        """
        Handles the case where the document type is a FGTS certificate.

        :return: The workflow.
        :rtype: Workflow
        """
        return FGTSWorkflowFactory().get_workflow()

    def get_workflow(self, cnpj: str, document_type: DocumentTypeEnum):
        """
        Selects the correct workflow based on the cnpj and document type.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :param document_type: The document type.
        :type document_type: DocumentTypeEnum
        :return: The workflow.
        :rtype: Workflow

        :raises MunicipioNotSupportedException: If the municipality is not supported.
        :raises DocumentTypeNotSupportedException: If the document type is not supported.
        :raises WorkflowSelectorException: If an unexpected error occurs.
        """
        try:
            validate_cnpj(cnpj)
            
            if not isinstance(document_type, DocumentTypeEnum):
                raise ValueError("document_type must be a DocumentTypeEnum")
            
            if document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL:
                return self._handle_municipal_workflow(cnpj)
            if document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS :
                return self._handle_fgts_workflow()
            else:
                raise DocumentTypeNotSupportedException("there is no workflow to download the certificate for the given document type: {}".format(document_type))
        
        except Exception as e:
            raise WorkflowSelectorException(e)
