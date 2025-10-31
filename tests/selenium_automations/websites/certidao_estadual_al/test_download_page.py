from pathlib import Path
import pytest
from unittest.mock import MagicMock

from selenium.webdriver.chrome.webdriver import WebDriver

from automacao_certificados.selenium_automations.websites.certidao_estadual_al.pages import DownloadPage
from automacao_certificados.selenium_automations.websites.certidao_estadual_al.exceptions import *

@pytest.fixture
def png_file_path(tmp_path: Path) -> Path:
    png_file_path = tmp_path / "test.png"
    png_file_path.touch()
    return png_file_path

class TestDownloadPage:
    
    def test_if_validate_img_path_raises_value_error_if_img_path_is_not_a_path_object(self, png_file_path: Path):
        with pytest.raises(ValueError) as e:
            DownloadPage(
                driver=MagicMock(spec=WebDriver),
            )._validate_img_path(img_path_to_save="invalid_path")

        assert "img_path_to_save" in str(e.value)


    def test_if_validate_img_path_raises_img_path_already_exists_exception_if_file_already_exists(
        self,
        png_file_path: Path,
    ):
        with pytest.raises(ImgPathAlreadyExistsException) as e:
            DownloadPage(
                driver=MagicMock(spec=WebDriver),
            )._validate_img_path(img_path_to_save=png_file_path)

        assert str(png_file_path) in str(e.value)

    def test_if_validate_img_path_raises_img_path_exception_if_file_parent_directory_does_not_exist(
        self,
        png_file_path: Path,
    ):
        with pytest.raises(ImgPathException) as e:
            DownloadPage(
                driver=MagicMock(spec=WebDriver),
            )._validate_img_path(img_path_to_save=Path("invalid_path/test.png"))

        assert "does not exist" in str(e.value)

    def test_if_validate_img_path_raises_img_path_exception_if_file_suffix_is_not_valid(
        self,
        png_file_path: Path,
    ):
        with pytest.raises(ImgPathException) as e:
            DownloadPage(
                driver=MagicMock(spec=WebDriver),
            )._validate_img_path(img_path_to_save=Path("test.txt"))

        assert "not valid" in str(e.value)

    