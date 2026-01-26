import pytest
from unittest.mock import Mock
import types
from urllib.parse import quote
from datetime import date

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.adapters.extractors import *
from automacao_certificados.selenium_automations.core.exceptions import *

class TestCertificadoDelmiroExtractor:
    """
    Test class for the CertificadoDelmiroExtractor class.
    """
    def test_if_raises_value_error_if_driver_is_not_a_web_driver(self):
        """
        Test if the CertificadoDelmiroExtractor raises a ValueError if the driver is not a WebDriver.
        """
        with pytest.raises(ValueError) as e:
            CertificadoDelmiroExtractor(driver="not_a_web_driver")
        assert "driver" in str(e.value)

    def test_if_get_supplier_name_raises_error_extracting_data_exception_if_error_extracting_data(
        self,
        monkeypatch,
    ):

        def mock_webdriver_wait_until(by, timeout):
            raise Exception("Error extracting data")

        monkeypatch.setattr(
            WebDriverWait,
            "until", 
            mock_webdriver_wait_until
        )

        extractor = CertificadoDelmiroExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor._get_supplier_name()

        assert "supplier_name" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_supplier_cnpj_raises_error_extracting_data_exception_if_error_extracting_data(
        self,
        monkeypatch,
    ):

        def mock_webdriver_wait_until(by, timeout):
            raise Exception("Error extracting data")

        monkeypatch.setattr(
            WebDriverWait,
            "until", 
            mock_webdriver_wait_until
        )

        extractor = CertificadoDelmiroExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor._get_supplier_cnpj()

        assert "cnpj" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_identifier_raises_error_extracting_data_exception_if_error_extracting_data(
        self,
        monkeypatch,
    ):

        def mock_webdriver_wait_until(by, timeout):
            raise Exception("Error extracting data")

        monkeypatch.setattr(
            WebDriverWait,
            "until", 
            mock_webdriver_wait_until
        )

        extractor = CertificadoDelmiroExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor.get_identifier()

        assert "identifier" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_expiration_date_raises_error_extracting_data_exception_if_error_extracting_data(
        self,
        monkeypatch,
    ):

        def mock_webdriver_wait_until(by, timeout):
            raise Exception("Error extracting data")

        monkeypatch.setattr(
            WebDriverWait,
            "until", 
            mock_webdriver_wait_until
        )

        extractor = CertificadoDelmiroExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor.get_expiration_date()

        assert "expiration_date" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_supplier_returns_correct_supplier(self):
        extractor = CertificadoDelmiroExtractor(driver=Mock(spec=WebDriver))

        # bind mock methods
        extractor._get_supplier_cnpj = types.MethodType(lambda self: "17.503.314/0001-00", extractor)

        supplier = extractor.get_supplier()

        assert isinstance(supplier, dto_supplier.Supplier)
        assert supplier.cnpj == "17.503.314/0001-00"

    def test_if_get_document_type_returns_correct_document_type(self):
        extractor = CertificadoDelmiroExtractor(driver=Mock(spec=WebDriver))
        assert extractor.get_document_type() == "Certidão Negativa Municipal"

class TestCertificadoDelmiroExtractorRun:
    """
    Test class for the CertificadoDelmiroExtractor.run() method.
    """
    def test_sucess_cases(self):
        from selenium import webdriver
        
        HTML_SOURCES = [
            """\
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="utf-8">
                <title>Certidão Negativa de Débitos - Delmiro Gouveia</title>
            </head>
            <body>
                <div id="MvcViewerReportPanel">
                    <table>
                        <tbody>
                            <tr>
                                <td colspan="2" style="text-align: center;">
                                    <strong>ESTADO DE ALAGOAS</strong><br>
                                    <strong>PREFEITURA MUNICIPAL DE DELMIRO GOUVEIA</strong><br>
                                    <strong>CERTIDÃO NEGATIVA DE DÉBITOS</strong>
                                </td>
                            </tr>
                            <tr>
                                <td><strong>Número:</strong></td>
                                <td>461/2026</td>
                            </tr>
                            <tr>
                                <td><strong>Liberada:</strong></td>
                                <td>26/01/2026</td>
                            </tr>
                            <tr>
                                <td><strong>Validade:</strong></td>
                                <td>27/03/2026</td>
                            </tr>
                            <tr>
                                <td><strong>Processo:</strong></td>
                                <td>Não informado</td>
                            </tr>
                            <tr>
                                <td colspan="2"><strong>Dados do econômico:</strong></td>
                            </tr>
                            <tr>
                                <td><strong>Inscritão municipal:</strong></td>
                                <td>402495</td>
                            </tr>
                            <tr>
                                <td><strong>Nome do econômico:</strong></td>
                                <td>CREARE CONSULTORES ASSOCIADOS</td>
                            </tr>
                            <tr>
                                <td><strong>Atividade principal:</strong></td>
                                <td>0360 - Ensino técnico, profissionalizante e preparatório</td>
                            </tr>
                            <tr>
                                <td><strong>Endereço:</strong></td>
                                <td>Rua Angelita Oliveira De Souza, nº 123 Centro - Delmiro Gouveia - Alagoas - CEP 57480-000</td>
                            </tr>
                            <tr>
                                <td colspan="2"><strong>Informação empresarial:</strong></td>
                            </tr>
                            <tr>
                                <td><strong>Nome empresarial:</strong></td>
                                <td>CREARE CONSULTORIA E ASSESSORIA EMPRESARIAL E PESSOAL S/S</td>
                            </tr>
                            <tr>
                                <td><strong>CPF/CNPJ:</strong></td>
                                <td>17.503.314/0001-00</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """,
            # Test case with "Nome do econômico:" and "CPF/CNPJ:" in same cell
            """\
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="utf-8">
                <title>Certidão Negativa de Débitos - Delmiro Gouveia</title>
            </head>
            <body>
                <div id="MvcViewerReportPanel">
                    <table>
                        <tbody>
                            <tr>
                                <td colspan="2" style="text-align: center;">
                                    <strong>CERTIDÃO NEGATIVA DE DÉBITOS</strong>
                                </td>
                            </tr>
                            <tr>
                                <td>Número: 461/2026</td>
                                <td></td>
                            </tr>
                            <tr>
                                <td>Validade: 27/03/2026</td>
                                <td></td>
                            </tr>
                            <tr>
                                <td>Nome do econômico: CREARE CONSULTORES ASSOCIADOS</td>
                                <td></td>
                            </tr>
                            <tr>
                                <td>CPF/CNPJ: 17.503.314/0001-00</td>
                                <td></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </body>
            </html>
            """,
            # Test case with Stimulsoft report viewer structure
            """\
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <style id="MvcViewerStyles" type="text/css" stimulsoft="stimulsoft">
                    .se050705f{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sf1f42b91{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sbeca8654{background-color:#FFFFFF;Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sa24c6805{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .s1393a43c{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .s4eaa60a2{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sba698e63{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .s976b941d{Font:bold 12pt Arial;border:0px;text-align:center;vertical-align:middle;}
                    .sa092a8ee{Font:bold 8pt Arial;border:0px;text-align:left;vertical-align:middle;}
                    .sb6838ca8{Font:8pt Arial;border:0px;text-align:left;vertical-align:middle;}
                </style>
            </head>
            <body>
                <div id="MvcViewer" style="background-color: white; height: 100%; width: 100%;">
                    <div id="MvcViewerReportPanel" class="stiJsViewerReportPanel">
                        <div class="stiJsViewerPage" style="overflow: hidden; margin: 10px auto; display: table; text-align: left; vertical-align: top; padding: 39px; border: 1px solid gray; background: white;">
                            <table cellspacing="0" cellpadding="0" border="0" style="border-width:0px;width:718px;border-collapse:collapse;">
                                <tbody>
                                    <tr>
                                        <td class="s976b941d" colspan="24">CERTIDÃO NEGATIVA DE DÉBITOS</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Número:</td>
                                        <td class="sb6838ca8">461/2026</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Validade:</td>
                                        <td class="sb6838ca8">27/03/2026</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Nome do econômico:</td>
                                        <td class="sb6838ca8">CREARE CONSULTORES ASSOCIADOS</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">CPF/CNPJ:</td>
                                        <td class="sb6838ca8">17.503.314/0001-00</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """,
            # Test case with more complex Stimulsoft structure (multiple rows, nested cells)
            """\
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <style id="MvcViewerStyles" type="text/css" stimulsoft="stimulsoft">
                    .se050705f{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sf1f42b91{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sbeca8654{background-color:#FFFFFF;Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sa24c6805{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .s1393a43c{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;word-wrap:break-word;}
                    .s4eaa60a2{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .sba698e63{Font:8pt Arial;border:0px;text-align:left;vertical-align:top;}
                    .s976b941d{Font:bold 12pt Arial;border:0px;text-align:center;vertical-align:middle;}
                    .sa092a8ee{Font:bold 8pt Arial;border:0px;text-align:left;vertical-align:middle;}
                    .sb6838ca8{Font:8pt Arial;border:0px;text-align:left;vertical-align:middle;}
                </style>
            </head>
            <body>
                <div id="MvcViewer" style="background-color: white; height: 100%; width: 100%;">
                    <div id="MvcViewerReportPanel" class="stiJsViewerReportPanel">
                        <div class="stiJsViewerPage" style="overflow: hidden; margin: 10px auto; display: table; text-align: left; vertical-align: top; padding: 39px; border: 1px solid gray; background: white;">
                            <table cellspacing="0" cellpadding="0" border="0" style="border-width:0px;width:718px;border-collapse:collapse;">
                                <tbody>
                                    <tr style="height:8px;">
                                        <td class="se050705f" colspan="24" style="width:717px;height:7px;"></td>
                                    </tr>
                                    <tr style="height:90px;">
                                        <td class="sf1f42b91" colspan="2" style="width:8px;height:90px;"></td>
                                        <td class="sbeca8654" colspan="20" style="height:90px;">
                                            <strong>ESTADO DE ALAGOAS</strong><br>
                                            <strong>PREFEITURA MUNICIPAL DE DELMIRO GOUVEIA</strong><br>
                                            <strong>CERTIDÃO NEGATIVA DE DÉBITOS</strong>
                                        </td>
                                        <td class="s4eaa60a2" colspan="2" style="width:8px;height:90px;"></td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Número:</td>
                                        <td class="sb6838ca8" colspan="23">461/2026</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Liberada:</td>
                                        <td class="sb6838ca8" colspan="23">26/01/2026</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Validade:</td>
                                        <td class="sb6838ca8" colspan="23">27/03/2026</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee" colspan="24">Dados do econômico:</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Inscritão municipal:</td>
                                        <td class="sb6838ca8" colspan="23">402495</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Nome do econômico:</td>
                                        <td class="sb6838ca8" colspan="23">CREARE CONSULTORES ASSOCIADOS</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee" colspan="24">Informação empresarial:</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">Nome empresarial:</td>
                                        <td class="sb6838ca8" colspan="23">CREARE CONSULTORIA E ASSESSORIA EMPRESARIAL E PESSOAL S/S</td>
                                    </tr>
                                    <tr>
                                        <td class="sa092a8ee">CPF/CNPJ:</td>
                                        <td class="sb6838ca8" colspan="23">17.503.314/0001-00</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """,
        ]

        driver = webdriver.Chrome()
        for html_source in HTML_SOURCES:
            driver.get("data:text/html;charset=utf-8," + quote(html_source))
            extractor = CertificadoDelmiroExtractor(driver=driver)
            document = extractor.run()
            #assert document.supplier.name == "CREARE CONSULTORES ASSOCIADOS"
            assert document.supplier.cnpj == "17.503.314/0001-00"
            assert document.document_type == "Certidão Negativa Municipal"
            assert document.identifier == "461/2026"
            assert document.expiration_date == date(2026, 3, 27)
