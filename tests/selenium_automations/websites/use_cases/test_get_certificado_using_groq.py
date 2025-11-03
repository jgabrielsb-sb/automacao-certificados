from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.chrome.options import Options

import pytest
from unittest.mock import Mock

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.use_cases import get_certificado_using_groq
from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import BaseImageProcessor

@pytest.fixture
def driver() -> WebDriver:
    return WebDriver()

@pytest.fixture
def headless_driver() -> WebDriver:
    options = Options()
    options.add_argument("--headless")
    return WebDriver(options=options)

class TestBasicGetCertificadoUsingGroq:
    def test_if_raises_value_error_if_driver_is_not_a_webdriver_object(self):
        with pytest.raises(ValueError) as e:
            get_certificado_using_groq(
                driver="invalid_driver",
                state_value="AL",
                inscricao_value="12345678901234",
                img_path_to_save=Path("test.png"),
            )
        assert "driver" in str(e.value)

    def test_if_raises_value_error_if_state_value_is_not_a_string(self):
        with pytest.raises(ValueError) as e:
            get_certificado_using_groq(
                driver=WebDriver(),
                state_value=12345678901234,
                inscricao_value="12345678901234",
                img_path_to_save=Path("test.png"),
            )
        assert "state_value" in str(e.value)

    def test_if_raises_value_error_if_inscricao_value_is_not_a_string(self):
        with pytest.raises(ValueError) as e:
            get_certificado_using_groq(
                driver=WebDriver(),
                state_value="AL",
                inscricao_value=12345678901234,
                img_path_to_save=Path("test.png"),
            )
        assert "inscricao_value" in str(e.value)

    def test_if_raises_value_error_if_img_path_to_save_is_not_a_path_object(self):
        with pytest.raises(ValueError) as e:
            get_certificado_using_groq(
                driver=WebDriver(),
                state_value="AL",
                inscricao_value="12345678901234",
                img_path_to_save="invalid_img_path_to_save",
            )
        assert "img_path_to_save" in str(e.value)

class TestGetCertificadoUsingGroq:
    # case when complete cnpj in inserted --> full cnpj
    @pytest.mark.selenium_workflow_tests
    def test_if_download_certificado_by_cnpj_raises_incorrect_cnpj_exception_if_cnpj_is_not_correct(self, driver: WebDriver):
        with pytest.raises(IncorrectCNPJException):
            get_certificado_using_groq(
                driver=driver,
                state_value="AL",
                inscricao_value="12345678901234",
                img_path_to_save=Path("test.png"),
            )
            driver.quit()

    # case when cnpj does not have certificado
    @pytest.mark.selenium_workflow_tests
    def test_if_download_certificado_by_cnpj_raises_not_found_on_uf_exception_if_cnpj_is_not_found_on_uf(self, driver: WebDriver):
        with pytest.raises(NotFoundOnUFException):
            get_certificado_using_groq(
                driver=driver,
                state_value="AL",
                inscricao_value="12345678",
                img_path_to_save=Path("test.png"),
            )
            driver.quit()
    # case when img path already exists
    @pytest.mark.selenium_workflow_tests
    def test_if_download_certificado_by_cnpj_raises_img_path_already_exists_exception_if_img_path_already_exists(
        self, 
        driver: WebDriver,
        tmp_path: Path,
    ):
        img_path_to_save = tmp_path / "test.png"
        img_path_to_save.touch()

        with pytest.raises(ImgPathAlreadyExistsException):
            get_certificado_using_groq(
                driver=driver,
                state_value="AL",
                inscricao_value="60604235",
                img_path_to_save=img_path_to_save,
            )
            driver.quit()
    # case when img path parent directory does not exist
    @pytest.mark.selenium_workflow_tests
    def test_if_download_certificado_by_cnpj_raises_img_path_exception_if_parent_directory_does_not_exist(self, driver: WebDriver, tmp_path: Path):
        img_path_to_save = tmp_path / "invalid_path" / "test.png"
        with pytest.raises(ImgPathException):
            get_certificado_using_groq(
                driver=driver,
                state_value="AL",
                inscricao_value="60604235",
                img_path_to_save=img_path_to_save,
            )
            driver.quit()
    # case when img path suffix is not valid
    @pytest.mark.selenium_workflow_tests
    def test_if_download_certificado_by_cnpj_raises_img_path_exception_if_suffix_is_not_valid(self, driver: WebDriver, tmp_path: Path):
        img_path_to_save = tmp_path / "test.txt"
        with pytest.raises(ImgPathException):
            get_certificado_using_groq(
                driver=driver,
                state_value="AL",
                inscricao_value="60604235",
                img_path_to_save=img_path_to_save,
            )
            driver.quit()

    @pytest.mark.selenium_workflow_tests
    def test_if_get_certificado_using_groq_correctly(
        self, 
        driver: WebDriver, 
        tmp_path: Path
    ):
        img_path_to_save = tmp_path / "test.png"
        get_certificado_using_groq(
            driver=driver,
            state_value="AL",
            inscricao_value="60604235",
            img_path_to_save=img_path_to_save,
        )
        assert img_path_to_save.exists()
        assert img_path_to_save.is_file()
        driver.quit()
