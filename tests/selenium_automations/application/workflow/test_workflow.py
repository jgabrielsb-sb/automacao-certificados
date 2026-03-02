from automacao_certificados.selenium_automations.adapters.persistance import certificado_api_persistance
from automacao_certificados.selenium_automations.application.workflow.workflow import Workflow
from automacao_certificados.selenium_automations.core.exceptions.interfaces.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *
import pytest
from unittest.mock import Mock, MagicMock, patch

from automacao_certificados.selenium_automations.core.models.interfaces.dto_workflow import StepResult
from automacao_certificados.selenium_automations.adapters.persistance.certificado_api_persistance import CertificadoApiPersistance
from automacao_certificados.selenium_automations.adapters.persistance.ppe_persistance import PPEPersistance
@pytest.fixture
def workflow():
    return Workflow(
        document_downloader=Mock(spec=DocumentDownloaderPort),
        certificado_api_persistance=Mock(spec=CertificadoApiPersistance),
        ppe_api_persistance=Mock(spec=PPEPersistance)
    )

class TestWorkflow:
    def test_if_raises_value_error_if_document_downloader_is_not_a_document_downloader_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=None,
                certificado_api_persistance=Mock(spec=CertificadoApiPersistance),
                ppe_api_persistance=Mock(spec=PPEPersistance),
            )
        assert "document_downloader must be a DocumentDownloaderPort" in str(e.value)

    def test_if_raises_value_error_if_certificado_api_persistance_is_not_a_certificado_api_persistance_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=Mock(spec=DocumentDownloaderPort),
                certificado_api_persistance=None,
                ppe_api_persistance=Mock(spec=PPEPersistance),
            )
        assert "certificado_api_persistance must be a CertificadoApiPersistance" in str(e.value)

    def test_if_raises_value_error_if_ppe_api_persistance_is_not_a_certificado_api_persistance_port(self):
        with pytest.raises(ValueError) as e:
            Workflow(
                document_downloader=Mock(spec=DocumentDownloaderPort),
                certificado_api_persistance=Mock(spec=CertificadoApiPersistance),
                ppe_api_persistance=None,
            )
        assert "ppe_api_persistance must be a PPEPersistance" in str(e.value)

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
        certificado_api_persistance = MagicMock(spec=CertificadoApiPersistance)
        certificado_api_persistance.run.side_effect = DocumentPersistanceException('test excep')
        monkeypatch.setattr(workflow, "certificado_api_persistance", certificado_api_persistance)
        step_result = workflow.persist_data_in_certificado_api("test")

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
        certificado_api_persistance = MagicMock(spec=CertificadoApiPersistance)
        certificado_api_persistance.run.return_value = "sucess"
        monkeypatch.setattr(workflow, "certificado_api_persistance", certificado_api_persistance)
        step_result = workflow.persist_data_in_certificado_api("test")

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
        ppe_api_persistance = MagicMock(spec=PPEPersistance)
        ppe_api_persistance.run.side_effect = DocumentPersistanceException('test excep')
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        step_result = workflow.persist_data_in_ppe_api("test")

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
        ppe_api_persistance = MagicMock(spec=PPEPersistance)
        ppe_api_persistance.run.return_value = "sucess"
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        step_result = workflow.persist_data_in_ppe_api("test")

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

        certificado_api_persistance = MagicMock(spec=CertificadoApiPersistance)
        certificado_api_persistance.run.return_value = StepResult(sucess=True, error_message=None, output="sucess")

        ppe_api_persistance = MagicMock(spec=PPEPersistance)
        ppe_api_persistance.run.return_value = StepResult(sucess=True, error_message=None, output="sucess")

        monkeypatch.setattr(workflow, "document_downloader", document_downloader)
        monkeypatch.setattr(workflow, "certificado_api_persistance", certificado_api_persistance)
        monkeypatch.setattr(workflow, "ppe_api_persistance", ppe_api_persistance)
        
        workflow_output = workflow.run("test")

        assert workflow_output == WorkflowOutput(
            download_output_result=StepResult(sucess=True, error_message=None, output=document_downloader.run.return_value),
            persistance_output_result=StepResult(sucess=True, error_message=None, output=certificado_api_persistance.run.return_value),
            ppe_output_result=StepResult(sucess=True, error_message=None, output=ppe_api_persistance.run.return_value),
        )

    def test_if_run_returns_correct_workflow_output_result_when_certificado_api_persistance_fails(
        self,
        workflow: Workflow,
        monkeypatch
    ):
        document_extracted = DocumentExtracted(
            supplier=Supplier(cnpj='12345678912345'),
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_MUNICIPAL.value,
            identifier='test',
            expiration_date=date(2025, 1, 1)
        )
        perform_download_result = StepResult(
            output=DocumentDownloaderOutput(
                document_extracted=document_extracted,
                base64_pdf="test"
            ),
            sucess=True,
            error_message=None,
        )

        certificado_api_persistance_result = StepResult(
            output=None,
            sucess=False,
            error_message="test error"
        )

        with (
            patch.object(workflow,"perform_download",return_value=perform_download_result),
            patch.object(workflow,"persist_data_in_certificado_api", return_value=certificado_api_persistance_result)
        ):
            result = workflow.run(cnpj="test")
            
            assert isinstance(result, WorkflowOutput)
            
            assert isinstance(result.ppe_output_result, StepResult)
            assert result.ppe_output_result.sucess == False
            assert "Erro ao persistir a certidão na API de Certidões" in result.ppe_output_result.error_message
            assert result.ppe_output_result.output is None

        

        
        
