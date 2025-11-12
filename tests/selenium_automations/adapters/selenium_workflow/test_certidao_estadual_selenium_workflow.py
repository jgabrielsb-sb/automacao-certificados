
from automacao_certificados.selenium_automations.websites.certidao_estadual_al import *

from automacao_certificados.selenium_automations.core.interfaces import (
    ImageProcessorPort,
    CaptchaGatewayPort,
    SeleniumWorkflowInput, 
    SeleniumWorkflowOutput
)

from automacao_certificados.selenium_automations.adapters import (
    GroqImageProcessor,
    SeleniumCaptchaGateway,
    CertidaoEstadualALSeleniumWorkflow, 
)

from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document
)

from automacao_certificados.config import settings

import pytest

from groq import Groq

from unittest.mock import (
    MagicMock,
    Mock, 
    patch
)
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By

class TestInit:
    def test_if_raises_value_error_if_img_path_to_save_file_is_not_path(
        self
    ):
        with pytest.raises(ValueError) as e:
            CertidaoEstadualALSeleniumWorkflow(
                img_path_to_save_file="not path",
                driver=Mock(spec=WebDriver),
                image_processor=Mock(spec=ImageProcessorPort),
                captcha_gateway=Mock(spec=CaptchaGatewayPort)
            )

        assert "img_path_to_save_file" in str(e.value)

    def test_if_raises_value_error_if_image_processor_is_not_image_processor_port(
        self
    ):
        with pytest.raises(ValueError) as e:
            CertidaoEstadualALSeleniumWorkflow(
                img_path_to_save_file="path",
                driver=Mock(spec=WebDriver),
                image_processor="not image processor port",
                captcha_gateway=Mock(spec=CaptchaGatewayPort)
            )

        assert "image_processor" in str(e.value)

    def test_if_raises_value_error_if_captcha_gateway_is_not_captcha_gateway_port(
        self
    ):
        with pytest.raises(ValueError) as e:
            CertidaoEstadualALSeleniumWorkflow(
                img_path_to_save_file="path",
                driver=Mock(spec=WebDriver),
                image_processor=Mock(spec=ImageProcessorPort),
                captcha_gateway="not captcha gateway port"
            )

        assert "captcha_gateway" in str(e.value)

class TestHandleCaptcha:
    def test_if_retries_solving_captcha_until_solved(self, mocker):
        run_consulta_page = "automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages.consulta_page.ConsultaPage.run"
        mocker.patch(run_consulta_page, side_effect=[
            InvalidCaptchaException("test"),
            InvalidCaptchaException("test"),
            None
        ])
            
        selenium_workflow = CertidaoEstadualALSeleniumWorkflow(
            driver=MagicMock(spec=WebDriver),
            img_path_to_save_file=MagicMock(spec=Path),
            image_processor=MagicMock(spec=ImageProcessorPort),
            captcha_gateway=MagicMock(spec=CaptchaGatewayPort),
        )

        attempts = selenium_workflow._solve_captcha("12345678912")
        assert attempts == 2

class TestGetDocument:
    def test_sucess(self, monkeypatch, mocker):
        from datetime import date

        selenium_workflow = CertidaoEstadualALSeleniumWorkflow(
            driver=MagicMock(spec=WebDriver),
            img_path_to_save_file=MagicMock(spec=Path),
            image_processor=MagicMock(spec=ImageProcessorPort),
            captcha_gateway=MagicMock(spec=CaptchaGatewayPort),
        )
        cnpj = "12345678912"
        
        input = SeleniumWorkflowInput(
            supplier_cnpj=cnpj
        )

        def fake_solve_captcha(cnpj):
            return 2

        monkeypatch.setattr(
            selenium_workflow, 
            "_solve_captcha",
            fake_solve_captcha
        )

        run_download_page = "automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages.download_page.DownloadPage.run"
        mocker.patch(
            run_download_page, 
            return_value=[
                dto_document.DocumentExtracted(
                    supplier=dto_supplier.Supplier(
                        cnpj=cnpj
                    ),
                    document_type="TEST",
                    identifier="TEST",
                    expiration_date=date(2025, 1, 1)
                ), 
                "base64"
            ]
        )
         
        result = selenium_workflow.get_document(input)

        assert isinstance(result, SeleniumWorkflowOutput)
        assert result.document == dto_document.DocumentExtracted(
                    supplier=dto_supplier.Supplier(
                        cnpj=cnpj
                    ),
                    document_type="TEST",
                    identifier="TEST",
                    expiration_date=date(2025, 1, 1)
                )
        assert result.base64_pdf == "base64"

class TestWithPracticalExamples:
    @pytest.fixture
    def certificado_estadual(self, tmp_path):
        driver = WebDriver()

        CertidaoEstadualALSeleniumWorkflow(
            driver=driver,
            image_processor=GroqImageProcessor(
                client=Groq(api_key=settings.groq_api_key)
            ),
            captcha_gateway=SeleniumCaptchaGateway(
                webdriver=driver,
                img_locator=(
                    By.XPATH,
                    '//div[@class="captcha-imagem"]/img'
                ),
                input_locator=(
                    By.XPATH,
                    '//div[@class="captcha-texto"]/input'
                )
            )
        )
    def test_if_raises_not_basic_cnpj_when_not_basic_cnpj(self, certificado_estadual):
        cnpj = 14876384000115
        
        input = SeleniumWorkflowInput(
            supplier_cnpj=cnpj
        )
        certificado_estadual.get_document(input)

        

    def test_if_raises_incorrect_cnpj_when_incorrect_cnpj(self):
        pass

    def test_if_raises_not_found_on_uf_if_cnpj_not_found_on_uf(self):
        pass

    def test_sucess_case(self):
        pass



        



       
        




    
