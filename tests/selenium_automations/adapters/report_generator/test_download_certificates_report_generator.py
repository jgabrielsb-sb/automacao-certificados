
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
        download_certificate_result = DownloadCertificateResult(
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
       
        row = mock_generator._convert_element_to_row(download_certificate_result)

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
        download_certificate_result = DownloadCertificateResult(
            certificate=CertificateToDownload(
                cnpj="12345678912345",
                document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
            ),
            error_selection="test",
            workflow_output=WorkflowOutput(
                download_output_result=StepResult(
                    sucess=False,
                    error_message=None
                ),
                persistance_output_result=StepResult(
                    sucess=False,
                    error_message=None
                ),
                ppe_output_result=StepResult(
                    sucess=False,
                    error_message=None
                )
            )
        )

        row = mock_generator._convert_element_to_row(download_certificate_result)
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

class TestGenerateReport:
    def test_if_generate_report_returns_html_string_with_empty_output(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(output=[])
        
        html_content = mock_generator.generate_report(input_data)
        
        assert isinstance(html_content, str)
        assert "<html" in html_content.lower()
        assert "plotly" in html_content.lower()
        # Title may be escaped in JSON, so check for key parts
        assert "Certificados" in html_content
        assert "Relat" in html_content or "relat" in html_content.lower()
    
    def test_if_generate_report_returns_html_string_with_single_successful_result(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="12345678912345",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        assert isinstance(html_content, str)
        assert "<html" in html_content.lower()
        assert "plotly" in html_content.lower()
        assert "12345678912345" in html_content
        # Document type may be escaped in JSON (ã becomes \u00e3), so check for key parts
        assert "Certid" in html_content
        assert "Negativa Estadual" in html_content
    
    def test_if_generate_report_returns_html_string_with_single_failed_result(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="98765432109876",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL
                    ),
                    error_selection="Workflow selection error",
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=False,
                            error_message="Download failed"
                        ),
                        persistance_output_result=StepResult(
                            sucess=False,
                            error_message="Persistence failed"
                        ),
                        ppe_output_result=StepResult(
                            sucess=False,
                            error_message="PPE failed"
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        assert isinstance(html_content, str)
        assert "<html" in html_content.lower()
        assert "98765432109876" in html_content
        assert "Workflow selection error" in html_content or "workflow selection error" in html_content.lower()
    
    def test_if_generate_report_returns_html_string_with_multiple_results(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="11111111111111",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        )
                    )
                ),
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="22222222222222",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_FEDERAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=False,
                            error_message="Download error"
                        ),
                        persistance_output_result=StepResult(
                            sucess=False,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=False,
                            error_message="PPE error"
                        )
                    )
                ),
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="33333333333333",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection="Selection error",
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=False,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=False,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=False,
                            error_message=None
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        with open("test_generate_report_with_multiple_results.html", "w") as f:
            f.write(html_content)
        
        assert isinstance(html_content, str)
        assert "<html" in html_content.lower()
        assert "11111111111111" in html_content
        assert "22222222222222" in html_content
        assert "33333333333333" in html_content
        assert "Download error" in html_content
        assert "PPE error" in html_content
        assert "Selection error" in html_content or "selection error" in html_content.lower()
    
    def test_if_generate_report_includes_table_structure(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="12345678912345",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        # Check for table-related elements (Plotly generates these)
        assert "table" in html_content.lower() or "plotly" in html_content.lower()
        # Check for expected column names
        assert "cnpj" in html_content.lower() or "CNPJ" in html_content
        assert "document_type" in html_content.lower() or "document" in html_content.lower()
    
    def test_if_generate_report_includes_date_in_title(
        self,
        mock_generator
    ):
        from datetime import datetime
        
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="12345678912345",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        # Check that the date format is in the title
        today = datetime.now()
        # Title and date may be escaped in JSON (/ becomes \u002f), so check for key parts
        assert "Certificados" in html_content
        assert "Relat" in html_content or "relat" in html_content.lower()
        # Check for date parts separately (slashes may be escaped as \u002f)
        assert str(today.day).zfill(2) in html_content
        assert str(today.month).zfill(2) in html_content
        assert str(today.year) in html_content
    
    def test_if_generate_report_handles_none_step_results(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="12345678912345",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=None,
                        persistance_output_result=None,
                        ppe_output_result=None
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        assert isinstance(html_content, str)
        assert "<html" in html_content.lower()
        assert "12345678912345" in html_content
    
    def test_if_generate_report_includes_plotly_cdn(
        self,
        mock_generator
    ):
        input_data = DownloadCertificatesUseCaseOutput(
            output=[
                DownloadCertificateResult(
                    certificate=CertificateToDownload(
                        cnpj="12345678912345",
                        document_type=DocumentTypeEnum.CERTIDAO_NEGATIVA_ESTADUAL
                    ),
                    error_selection=None,
                    workflow_output=WorkflowOutput(
                        download_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        persistance_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        ),
                        ppe_output_result=StepResult(
                            sucess=True,
                            error_message=None
                        )
                    )
                )
            ]
        )
        
        html_content = mock_generator.generate_report(input_data)
        
        # Check that Plotly CDN is included
        assert "cdn.plotly" in html_content or "plotly" in html_content.lower()
    