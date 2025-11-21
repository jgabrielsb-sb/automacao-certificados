from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.core.exceptions.interfaces.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
import pytest
from unittest.mock import Mock, MagicMock

from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import StepResult

@pytest.fixture
def workflow():
    return Workflow(
        document_downloader=Mock(spec=DocumentDownloaderPort),
        document_persistance=Mock(spec=DocumentPersistancePort),
        ppe_api_persistance=Mock(spec=DocumentPersistancePort)
    )

class TestWorkflow:
    def test_if_raises_value_error_if_document_downloader_is_not_a_document_downloader_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=None,
                document_persistance=Mock(spec=DocumentPersistancePort),
                ppe_api_persistance=Mock(spec=DocumentPersistancePort),
            )
        assert "document_downloader must be a DocumentDownloaderPort" in str(e.value)

    def test_if_raises_value_error_if_document_persistance_is_not_a_document_persistance_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=Mock(spec=DocumentDownloaderPort),
                document_persistance=None,
                ppe_api_persistance=Mock(spec=DocumentPersistancePort),
            )
        assert "document_persistance must be a DocumentPersistancePort" in str(e.value)

    def test_if_raises_value_error_if_ppe_api_persistance_is_not_a_document_persistance_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=Mock(spec=DocumentDownloaderPort),
                document_persistance=Mock(spec=DocumentPersistancePort),
                ppe_api_persistance=None,
            )
        assert "ppe_api_persistance must be a DocumentPersistancePort" in str(e.value)

    def test_if_perform_download_returns_step_result_when_error(
        self, 
        workflow,
        monkeypatch
    ):
        document_downloader = MagicMock(spec=DocumentDownloaderPort)
        document_downloader.run.side_effect = DocumentDownloaderException('test excep')
        
        monkeypatch.setattr(workflow, "document_downloader", document_downloader)

        step_result = workflow.perform_download("test")

        assert step_result == StepResult(
            sucess=False,
            error_message='test excep',
            output=None
        )

    def test_if_perform_download_returns_step_result_when_sucess(
        self, 
        workflow,
        monkeypatch
    ):
        document_downloader = MagicMock(spec=DocumentDownloaderPort)
        document_downloader.run.return_value = "sucess"
        monkeypatch.setattr(workflow, "document_downloader", document_downloader)

        step_result = workflow.perform_download("test")

        assert step_result == StepResult(
            sucess=True,
            error_message=None,
            output='sucess'
        )

    def test_if_persist_data_returns_step_result_when_error(
        self, 
        workflow,
        monkeypatch
    ):
        document_persistance = MagicMock(spec=DocumentPersistancePort)
        document_persistance.run.side_effect = DocumentPersistanceException('test excep')
        monkeypatch.setattr(workflow, "document_persistance", document_persistance)
        step_result = workflow.persist_data("test")

        assert step_result == StepResult(
            sucess=False,
            error_message='test excep',
            output=None
        )

    def test_if_persist_data_returns_step_result_when_sucess(
        self, 
        workflow,
        monkeypatch
    ):
        document_persistance = MagicMock(spec=DocumentPersistancePort)
        document_persistance.run.return_value = "sucess"
        monkeypatch.setattr(workflow, "document_persistance", document_persistance)
        step_result = workflow.persist_data("test")

        assert step_result == StepResult(
            sucess=True,
            error_message=None,
            output='sucess'
        )

    def test_if_persist_data_in_ppe_returns_step_result_when_error(
        self, 
        workflow,
        monkeypatch
    ):
        ppe_api_persistance = MagicMock(spec=DocumentPersistancePort)
        ppe_api_persistance.run.side_effect = DocumentPersistanceException('test excep')
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        step_result = workflow.persist_data_in_ppe("test")

        assert step_result == StepResult(
            sucess=False,
            error_message='test excep',
            output=None
        )

    def test_if_persist_data_in_ppe_returns_step_result_when_sucess(
        self, 
        workflow,
        monkeypatch
    ):
        ppe_api_persistance = MagicMock(spec=DocumentPersistancePort)
        ppe_api_persistance.run.return_value = "sucess"
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        step_result = workflow.persist_data_in_ppe("test")

        assert step_result == StepResult(
            sucess=True,
            error_message=None,
            output='sucess'
        )

    def test_if_run_returns_correct_workflow_output_result_when_download_fails(
        self,
        workflow,
        monkeypatch
    ):
        document_downloader = MagicMock(spec=DocumentDownloaderPort)
        document_downloader.run.side_effect = DocumentDownloaderException('test excep')
        monkeypatch.setattr(workflow, "document_downloader", document_downloader)
        step_result = workflow.run("test")

        assert step_result == WorkflowOutput(
            download_output_result=StepResult(sucess=False, error_message='test excep', output=None),
            persistance_output_result=None,
            ppe_output_result=None,
        )
    
    def test_if_run_returns_correct_workflow_output_result_when_all_steps_sucess(
        self,
        workflow,
        monkeypatch
    ):
        document_downloader = MagicMock(spec=DocumentDownloaderPort)
        document_extracted = DocumentExtracted(
            supplier=Supplier(cnpj='12345678912345'),
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL.value,
            identifier='test',
            expiration_date=date(2025, 1, 1)
        )
        document_downloader.run.return_value = DocumentDownloaderOutput(
            document_extracted=document_extracted,
            base64_pdf="test base64 pdf"
        )

        document_persistance = MagicMock(spec=DocumentPersistancePort)
        document_persistance.run.return_value = StepResult(sucess=True, error_message=None, output="sucess")

        ppe_api_persistance = MagicMock(spec=DocumentPersistancePort)
        ppe_api_persistance.run.return_value = StepResult(sucess=True, error_message=None, output="sucess")

        monkeypatch.setattr(workflow, "document_downloader", document_downloader)
        monkeypatch.setattr(workflow, "document_persistance", document_persistance)
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        
        workflow_output = workflow.run("test")

        assert workflow_output == WorkflowOutput(
            download_output_result=StepResult(sucess=True, error_message=None, output=document_downloader.run.return_value),
            persistance_output_result=StepResult(sucess=True, error_message=None, output=document_persistance.run.return_value),
            ppe_output_result=StepResult(sucess=True, error_message=None, output=ppe_api_persistance.run.return_value),
        )