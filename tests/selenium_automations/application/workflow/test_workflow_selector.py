from automacao_certificados.selenium_automations.application.workflow.factories import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *

import pytest
from unittest.mock import Mock

class TestWorkflowSelector:

    def test_if_raises_value_error_if_municipio_api_requester_is_not_a_municipio_getter_port(self):
        with pytest.raises(ValueError) as e:
            WorkflowSelector(
                municipio_api_requester="invalid"
            )

        assert "municipio_api_requester must be a MunicipioGetterPort" in str(e.value)

    def test_if_handle_municipal_workflow_returns_correct_workflow(self):
        mock_municipio_api_requester = Mock(spec=MunicipioGetterPort)
        mock_municipio_api_requester.run.return_value = "ARAPIRACA"
        
        workflow_selector = WorkflowSelector(mock_municipio_api_requester)

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)

    def test_if_raises_value_error_when_not_valid_municipio(self):
        mock_municipio_api_requester = Mock(spec=MunicipioGetterPort)
        mock_municipio_api_requester.run.return_value = MunicipioEnum.DELMIRO_GOUVEIA
        
        workflow_selector = WorkflowSelector(mock_municipio_api_requester)

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        
        assert "there is no workflow to download the certificate for the given municipality: {}".format(MunicipioEnum.DELMIRO_GOUVEIA) in str(e.value)

    def test_if_raises_value_error_when_document_type_is_not_a_document_type_enum(self):
        mock_municipio_api_requester = Mock(spec=MunicipioGetterPort)
        mock_municipio_api_requester.run.return_value = MunicipioEnum.ARAPIRACA
        
        workflow_selector = WorkflowSelector(mock_municipio_api_requester)

        cnpj = "12345678912345"
        document_type = "invalid"
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        assert "document_type must be a DocumentTypeEnum" in str(e.value)


    def test_if_raises_value_error_when_not_valid_document_type(self):
        mock_municipio_api_requester = Mock(spec=MunicipioGetterPort)
        mock_municipio_api_requester.run.return_value = MunicipioEnum.ARAPIRACA
        
        workflow_selector = WorkflowSelector(mock_municipio_api_requester)

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        
        assert "there is no workflow to download the certificate for the given document type: {}".format(document_type) in str(e.value)


        
        
