from pathlib import Path
import pytest
from unittest.mock import MagicMock

from selenium.webdriver.chrome.webdriver import WebDriver

from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.pages import DownloadPage
from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.exceptions import *

@pytest.fixture
def png_file_path(tmp_path: Path) -> Path:
    png_file_path = tmp_path / "test.png"
    png_file_path.touch()
    return png_file_path

class TestDownloadPage:
    pass
    
    

    