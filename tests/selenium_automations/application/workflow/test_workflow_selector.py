from automacao_certificados.selenium_automations.application.workflow.factories import *
from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.application import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.adapters import *
from automacao_certificados.selenium_automations.core.exceptions import *

import pytest
from unittest.mock import MagicMock, Mock

class TestWorkflowSelector:

    def test_if_raises_value_error_if_municipio_getter_port_is_not_a_municipio_getter_port(self):
        with pytest.raises(ValueError) as e:
            WorkflowSelector(
                municipio_getter_port="invalid",
                estado_getter_port=MagicMock(spec=EstadoGetterPort)
            )

        assert "municipio_getter_port must be a MunicipioGetterPort" in str(e.value)

    def test_if_raises_value_error_if_estado_getter_port_is_not_a_estado_getter_port(self):
        with pytest.raises(ValueError) as e:
            WorkflowSelector(
                municipio_getter_port=MagicMock(spec=MunicipioGetterPort),
                estado_getter_port="invalid"
            )

        assert "estado_getter_port must be a EstadoGetterPort" in str(e.value)

    def test_if_handle_municipal_workflow_returns_correct_workflow(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "ARAPIRACA"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)

    def test_if_raises_value_error_when_not_valid_municipio(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "INVALID"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        
        assert "there is no workflow to download the certificate for the given municipality: {}".format("INVALID") in str(e.value)

    def test_if_raises_value_error_when_document_type_is_not_a_document_type_enum(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "ARAPIRACA"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = "invalid"
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        assert "document_type must be a DocumentTypeEnum" in str(e.value)


    def test_if_raises_value_error_when_not_valid_document_type(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "ARAPIRACA"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.TEST_DOCUMENT
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        
        assert "there is no workflow to download the certificate for the given document type: {}".format(document_type) in str(e.value)

    def test_if_raises_value_error_when_not_valid_estado(self):
        mock_estado_getter_port = Mock(spec=EstadoGetterPort)
        mock_estado_getter_port.run.return_value = "INVALID"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=MagicMock(spec=MunicipioGetterPort),
            estado_getter_port=mock_estado_getter_port
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
        with pytest.raises(WorkflowSelectorException) as e:
            workflow = workflow_selector.get_workflow(cnpj, document_type)
        
        assert "there is no workflow to download the certificate for the given state: {}".format("INVALID") in str(e.value)

    def test_if_returns_arapiraca_workflow_when_municipio_is_arapiraca(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "ARAPIRACA"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)
        assert isinstance(workflow.document_downloader, DocumentArapiracaDownloader)

    def test_if_returns_maceio_workflow_when_municipio_is_maceio(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "MACEIO"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)
        assert isinstance(workflow.document_downloader, DocumentMaceioDownloader)

    def test_if_returns_delmiro_workflow_when_municipio_is_delmiro_gouveia(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "DELMIRO GOUVEIA"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)
        assert isinstance(workflow.document_downloader, DocumentDelmiroDownloader)

    def test_if_returns_penedo_workflow_when_municipio_is_penedo(self):
        mock_municipio_getter_port = Mock(spec=MunicipioGetterPort)
        mock_municipio_getter_port.run.return_value = "PENEDO"
        
        workflow_selector = WorkflowSelector(
            municipio_getter_port=mock_municipio_getter_port,
            estado_getter_port=MagicMock(spec=EstadoGetterPort)
        )

        cnpj = "12345678912345"
        document_type = DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL
        workflow = workflow_selector.get_workflow(cnpj, document_type)

        assert isinstance(workflow, Workflow)
        assert isinstance(workflow.document_downloader, DocumentPenedoDownloader)

        
