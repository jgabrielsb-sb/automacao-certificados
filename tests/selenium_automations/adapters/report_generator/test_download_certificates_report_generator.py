
import pytest

from automacao_certificados.selenium_automations.adapters import *

@pytest.fixture
def mock_generator():
    return DownloadCertificatesReportGenerator()

class TestIsStepSucess:
    def test_if_is_step_sucess_returns_correct_response_when_step_result_is_none(
        self,
        mock_generator
    ):
        step_result = None

        is_step_sucess = mock_generator._is_step_sucess(step_result)
        assert is_step_sucess == False

    def test_if_is_step_sucess_returns_correct_response_when_step_is_not_none(
        self,
        mock_generator
    ):
        step_result_true = StepResult(
            sucess=True,
            error_message=None
        )

        step_result_false = StepResult(
            sucess=False,
            error_message="test"
        )

        assert mock_generator._is_step_sucess(step_result_true) == True
        assert mock_generator._is_step_sucess(step_result_false) == False

class TestGetErrorMessage:
    def test_if_get_error_message_returns_correct_response_when_step_result_is_none(
        self,
        mock_generator
    ):
        step_result = None

        error_message = mock_generator._get_error_message(step_result)
        assert error_message == None

    def test_if_get_error_message_returns_correct_response_when_step_is_not_none(
        self,
        mock_generator
    ):
        step_result_true = StepResult(
            sucess=True,
            error_message=None
        )

        step_result_false = StepResult(
            sucess=False,
            error_message="test"
        )

        assert mock_generator._get_error_message(step_result_true) == None
        assert mock_generator._get_error_message(step_result_false) == "test"

class TestConvertElementToRow:
    def test_if_convert_element_to_row_returns_correct_response_when_element_is_not_none(
        self,
        mock_generator
    ):
        element = DownloadCertificatesUseCaseOutput(
            certificate=CertificateToDownload(
                cnpj="12345678912345",
                document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
            ),
            error_selection=None,
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=False,
                    error_message="test"
                ),
                persistance_output_result=StepResult(
                    sucess=False,
                    error_message="test"
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message="test"
                )
            )
        )

        row = mock_generator._convert_element_to_row(element)

        assert row == DownloadCertificatesRow(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL,
            error_selection=None,
            download_step_is_sucess=False,
            download_step_error_message="test",
            persistance_step_is_sucess=False,
            persistance_step_error_message="test",
            ppe_step_is_sucess=False,
            ppe_step_error_message="test"
        )
        assert row.model_dump(mode="json") == {
            "cnpj": "12345678912345",
            "document_type": "Certidão Negativa Estadual",
            "error_selection": None,
            "download_step_is_sucess": False,
            "download_step_error_message": "test",
            "persistance_step_is_sucess": False,
            "persistance_step_error_message": "test",
            "ppe_step_is_sucess": False,
            "ppe_step_error_message": "test",
        }

    def test_if_convert_element_to_row_returns_correct_response_when_element_is_none(
        self,
        mock_generator
    ):
        element = DownloadCertificatesUseCaseOutput(
            certificate=CertificateToDownload(
                cnpj="12345678912345",
                document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
            ),
            error_selection="test",
            workflow_output=WorkflowOutput(
                download_output_result=None,
                persistance_output_result=None,
                ppe_output_result=None
            )
        )

        row = mock_generator._convert_element_to_row(element)
        assert row == DownloadCertificatesRow(
            cnpj="12345678912345",
            document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL,
            error_selection="test",
            download_step_is_sucess=False,
            download_step_error_message=None,
            persistance_step_is_sucess=False,
            persistance_step_error_message=None,
            ppe_step_is_sucess=False,
            ppe_step_error_message=None
        )

        assert row.model_dump(mode="json") == {
            "cnpj": "12345678912345",
            "document_type": "Certidão Negativa Estadual",
            "error_selection": "test",
            "download_step_is_sucess": False,
            "download_step_error_message": None,
            "persistance_step_is_sucess": False,
            "persistance_step_error_message": None,
            "ppe_step_is_sucess": False,
            "ppe_step_error_message": None,
        }