from automacao_certificados.selenium_automations.application.workflow.factories import *
from automacao_certificados.selenium_automations.application.workflow.factories.federal_workflow_factory import FederalWorkflowFactory
from automacao_certificados.selenium_automations.application.workflow.factories.delmiro_workflow_factory import DelmiroWorkflowFactory

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.utils import validate_cnpj
from automacao_certificados.selenium_automations.core.exceptions import *

class WorkflowSelector:
    def __init__(
        self,
        municipio_getter_port: MunicipioGetterPort,
        estado_getter_port: EstadoGetterPort,
    ):
        """
        The workflow selector is responsible for selecting the correct workflow based on the cnpj and document type.

        """
        if not isinstance(municipio_getter_port, MunicipioGetterPort):
            raise ValueError("municipio_getter_port must be a MunicipioGetterPort")
        
        if not isinstance(estado_getter_port, EstadoGetterPort):
            raise ValueError("estado_getter_port must be a EstadoGetterPort")

        self.municipio_getter_port = municipio_getter_port
        self.estado_getter_port = estado_getter_port
        
    
    def _get_municipio_by_cnpj(self, cnpj: str) -> str:
        """
        Gets the municipality by cnpj using the municipio api requester.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :return: The municipality name.
        :rtype: str
        """
        municipio = self.municipio_getter_port.run(cnpj)
        return municipio

    def _get_estado_by_cnpj(self, cnpj: str) -> str:
        estado = self.estado_getter_port.run(cnpj)
        return estado

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
        if municipio == "DELMIRO GOUVEIA":
            return DelmiroWorkflowFactory().get_workflow()
        if municipio == "PENEDO":
            return PenedoWorkflowFactory().get_workflow()
        else:
            raise MunicipioNotSupportedException("there is no workflow to download the certificate for the given municipality: {}".format(municipio))

    def _handle_fgts_workflow(self):
        """
        Handles the case where the document type is a FGTS certificate.

        :return: The workflow.
        :rtype: Workflow
        """
        return FGTSWorkflowFactory().get_workflow()
    
    def _handle_federal_workflow(self):
        #raise NotImplementedError("not implemented to save tokens. remove the comment to reactivate this workflow")
        return FederalWorkflowFactory().get_workflow()

    def _handle_estadual_workflow(self, cnpj):
        estado = self._get_estado_by_cnpj(cnpj)

        if estado == 'AL':
            return AlagoasWorkflowFactory().get_workflow()
        else:
            raise EstadoNotSupportedException("there is no workflow to download the certificate for the given state: {}".format(estado))

    def get_municipio_for_certificate(self, cnpj: str, document_type: DocumentTypeEnum) -> str | None:
        """
        Gets the municipality name for a certificate if it's a municipal certificate.

        :param cnpj: The cnpj of the company.
        :type cnpj: str
        :param document_type: The document type.
        :type document_type: DocumentTypeEnum
        :return: The municipality name if it's a municipal certificate, None otherwise.
        :rtype: str | None
        """
        if document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL:
            try:
                return self._get_municipio_by_cnpj(cnpj)
            except Exception:
                return None
        return None

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
            elif document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL:
                return self._handle_estadual_workflow(cnpj)
            elif document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_FGTS:
                return self._handle_fgts_workflow()
            elif document_type == DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL:
                return self._handle_federal_workflow()
            else:
                raise DocumentTypeNotSupportedException("there is no workflow to download the certificate for the given document type: {}".format(document_type))
        
        except Exception as e:
            raise WorkflowSelectorException(e)
