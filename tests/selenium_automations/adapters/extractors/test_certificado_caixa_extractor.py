import pytest
from unittest.mock import Mock
import types
from urllib.parse import quote
from datetime import date

from automacao_certificados.selenium_automations.core.models import dto_supplier
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from automacao_certificados.selenium_automations.adapters.extractors import CertificadoCaixaExtractor
from automacao_certificados.selenium_automations.adapters.extractors.exceptions import ErrorExtractingDataException

class TestCertificadoCaixaExtractor:
    """
    Test class for the CertificadoCaixaExtractor class.
    """
    def test_if_raises_value_error_if_driver_is_not_a_web_driver(self):
        """
        Test if the CertificadoCaixaExtractor raises a ValueError if the driver is not a WebDriver.
        """
        with pytest.raises(ValueError) as e:
            CertificadoCaixaExtractor(driver="not_a_web_driver")
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

        extractor = CertificadoCaixaExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor._get_supplier_name()

        assert "razao_social" in str(e.value)
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

        extractor = CertificadoCaixaExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor._get_supplier_cnpj()

        assert "cnpj" in str(e.value)
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

        extractor = CertificadoCaixaExtractor(
            driver=Mock(spec=WebDriver),
        )

        with pytest.raises(ErrorExtractingDataException) as e:
            extractor.get_expiration_date()

        assert "expiration_date" in str(e.value)
        assert "Error extracting data" in str(e.value)

    def test_if_get_supplier_returns_correct_supplier(self):
        extractor = CertificadoCaixaExtractor(driver=Mock(spec=WebDriver))

        # bind mock methods
        extractor._get_supplier_name = types.MethodType(lambda self: "Test Supplier", extractor)
        extractor._get_supplier_cnpj = types.MethodType(lambda self: "Test CNPJ", extractor)

        supplier = extractor.get_supplier()

        assert isinstance(supplier, dto_supplier.Supplier)
        #assert supplier.name == "Test Supplier"
        assert supplier.cnpj == "Test CNPJ"

    def test_if_get_document_type_returns_correct_document_type(self):
        extractor = CertificadoCaixaExtractor(driver=Mock(spec=WebDriver))
        assert extractor.get_document_type() == "CERTIFICADO CAIXA"

class TestCertificadoCaixaExtractorRun:
    """
    Test class for the CertificadoCaixaExtractor.run() method.
    """
    def test_sucess_cases(self):
        from selenium import webdriver
        
        HTML_SOURCES = [
            """\
            <html xmlns="http://www.w3.org/1999/xhtml">
            <head>
                <meta charset="utf-8">
                <meta name="author" content="RQ_AOA">
                <meta name="description" content="Caixa Prototype">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta http-equiv="refresh" content="120;url=/consultacrf/pages/consultaEmpregador.jsf">
                
                <title>Consulta Regularidade do Empregador</title>
                <link class="component" href="/consultacrf/a4j/s/3_3_2.SR1org/richfaces/renderkit/html/css/basic_classes.xcss/DATB/eAELXT5DOhSIAQ!sA18_.jsf" rel="stylesheet" type="text/css">
                <link class="component" href="/consultacrf/a4j/s/3_3_2.SR1org/richfaces/renderkit/html/css/extended_classes.xcss/DATB/eAELXT5DOhSIAQ!sA18_.jsf" media="rich-extended-skinning" rel="stylesheet" type="text/css">
                <script src="/consultacrf/a4j/g/3_3_2.SR1org.ajax4jsf.javascript.AjaxScript.jsf" type="text/javascript"></script>
                <script src="/consultacrf/a4j/g/3_3_2.SR1org/ajax4jsf/javascript/scripts/form.js.jsf" type="text/javascript"></script>
                <script type="text/javascript">window.RICH_FACES_EXTENDED_SKINNING_ON=true;</script>
                <script src="/consultacrf/a4j/g/3_3_2.SR1org/richfaces/renderkit/html/scripts/skinning.js.jsf" type="text/javascript"></script>
                <style>
                    form {
                        padding: 2em 13%;
                    }
                    .submit-d {
                        position: relative;
                        display: inline-block;
                        height: 2.65em;
                        min-width: 6em;
                        width: 100%;
                        border-width: 1px;
                        border-style: solid;
                        padding: 0 1.5em;
                        border-radius: 2px;
                        box-shadow: 0px 2px 0 rgba(31,42,71,.1);
                        font-family: "FuturaWeb", sans-serif;
                        font-size: 1.125em;
                        line-height: 1;
                        outline: none;
                    }
                    
                    a.submit-d {
                        line-height: 2.8rem;
                        cursor: pointer;
                    }
                    
                    a.submit-small {
                        line-height: 2.6rem;
                    }
                    
                    a.submit-d:hover {
                        color: #fff;
                    }
                    
                    .submit-d:focus,
                    .submit-selected {
                        box-shadow: 5px 5px 5px rgba(0,0,0,.15) inset;
                    }
                    
                    .submit-non-fluid {
                        width: auto;
                    }
                    
                    .submit-left {
                        float:left;
                    }
                    
                    .submit-disabled {
                        border-color: #a5aab5 !important;
                        background: #fff;
                        background: -webkit-linear-gradient(top,#fff 0%, #e9e9ec 100%) !important;
                        background: linear-gradient(to bottom,#fff 0%, #e9e9ec 100%) !important;
                        color: #4c556c !important;
                        opacity: .4 !important;
                    }
                    
                    .submit-small {
                        font-size: 1em;
                    }
                    
                    .submit-big {
                        font-size: 1.2em;
                    }
                    
                    .submit-white {
                        border-color: #a5aab5;
                        background: -webkit-linear-gradient(top,#fff 0%, #e9e9ec 100%);
                        background: linear-gradient(to bottom,#fff 0%, #e9e9ec 100%);
                        color: #006bae;
                    }
                    
                    .submit-d.submit-transparent {
                        background: transparent;
                        border-color: transparent;
                        box-shadow: none;
                    }
                    
                    .submit-white:hover {
                        border-color: #8c909a;
                        background: -webkit-linear-gradient(top,#fff 0%, #f4f4f6 100%);
                        background: linear-gradient(to bottom,#fff 0%, #f4f4f6 100%);
                    }
                    
                    .submit-white:focus,
                    .submit-white.submit-selected {
                        background: #dcdddf;
                        border-top-color: #4c556c;
                        color: #005d98;
                    }
                    
                    .submit-blue {
                        border-color: #1f2a47;
                        background: -webkit-linear-gradient(top,#058ce0 0%, #047ecb 100%);
                        background: linear-gradient(to bottom,#058ce0 0%, #047ecb 100%);
                        color: #fff;
                    }
                    
                    .submit-blue:hover {
                        border-color: #171d2f;
                        background: -webkit-linear-gradient(top,#119af0 0%, #0f8cda 100%);
                        background: linear-gradient(to bottom,#119af0 0%, #0f8cda 100%);
                    }
                    
                    .submit-blue:focus,
                    .submit-blue.submit-selected {
                        background: #0b6daa;
                        border-top-color: #000;
                        color: #fff;
                    }
                    
                    .submit-orange {
                        background: -webkit-linear-gradient(top,#fda917 0%, #fc8f01 100%);
                        background: linear-gradient(to bottom,#fda917 0%, #fc8f01 100%);
                        border-color: #9f6705;
                        color: #fff;
                    }
                    
                    .submit-orange:hover {
                        border-color: #6c4105;
                        background: -webkit-linear-gradient(top,#ffb32d 0%, #ff9a00 100%);
                        background: linear-gradient(to bottom,#ffb32d 0%, #ff9a00 100%);
                    }
                    
                    .submit-orange:focus,
                    .submit-orange.submit-selected {
                        background: #dd790d;
                        border-top-color: #462d09;
                        color: #fff;
                    }
                </style>
                <script type="text/javascript">
                    var infoWindowAMShown = false;
                    var infoWindowAMTimer;
                    function showModalInfoWindow() {
                        infoWindowAMTimer = setTimeout("if(!infoWindowAMShown){Richfaces.showModalPanel('ajaxLoadingModalBox');infoWindowAMShown=true;}", 500);
                    }
                    function hideModalInfoWindow() {
                        if (infoWindowAMShown) {
                            Richfaces.hideModalPanel('ajaxLoadingModalBox');
                            infoWindowAMShown=false;
                        } else {
                            if(infoWindowAMTimer)
                                clearTimeout(infoWindowAMTimer);
                        }
                    }
                    function Imprimir() {
                        window.print();
                    }
                </script>
            </head>
            <body>
                <!-- bloco principal -->
                <span id="mainOutputPanel">
                    <div class="form-wrapper">
                        <form id="mainForm" name="mainForm" method="post" action="/consultacrf/pages/impressao.jsf" target="">
                            <table width="75%">
                                <tbody>
                                    <tr>
                                        <td width="50%"></td>
                                        <td width="15%">
                                            <input id="mainForm:btVoltar3" type="submit" name="mainForm:btVoltar3" value="Voltar" class="submit-d submit-blue submit-small">
                                        </td>
                                        <td width="15%">
                                            <input id="mainForm:btImprimir4" type="submit" name="mainForm:btImprimir4" value="Imprimir" class="submit-d submit-blue submit-small" onclick="Javascript:Imprimir()">
                                        </td>
                                        <td></td>
                                    </tr>
                                </tbody>
                            </table>
                            <br><br>
                            <table width="100%" cellspacing="0" cellpadding="0" class="txtcentral" style="border: 1px solid black;" align="center">
                                <tbody>
                                    <tr>
                                        <td>
                                            <table width="100%" cellspacing="0" cellpadding="0" class="txtcentral">
                                                <tbody>
                                                    <tr>
                                                        <td width="40%"></td>
                                                        <td width="10%"></td>
                                                        <td></td>
                                                    </tr>
                                                    <tr>
                                                        <td align="left" style="padding: 15px;">
                                                            <img border="0" src="../estaticos/img/caixa.gif" width="180" height="44" alt="caixa">
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="padding: 15px;">
                                                            <span style="font-size: 13pt" align="center">
                                                                <strong>Certificado de Regularidade do FGTS - CRF</strong>
                                                            </span>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                            <table width="100%" cellspacing="0" cellpadding="0" class="txtcentral">
                                                <tbody>
                                                    <tr>
                                                        <td style="padding: 15px;" colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td width="22%">
                                                            <font style="font-family:Verdana;font-size:10pt;padding: 15px;">
                                                                <strong>Inscrição:</strong>
                                                            </font>
                                                        </td>
                                                        <td>
                                                            <font style="font-family: Verdana;font-size:8pt">
                                                                <span class="valor">60.604.235/0001-14</span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td width="22%" valign="top">
                                                            <font style="font-family: Verdana;font-size:10pt;padding: 15px;">
                                                                <strong>Razão Social:</strong>
                                                            </font>
                                                        </td>
                                                        <td>
                                                            <font style="font-family: Verdana;font-size:8pt">
                                                                <span class="valor">BUYERS CONSULTORIA ESTRATEGICA LTDA</span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td width="22%" valign="top">
                                                            <font style="font-family: Verdana;font-size:10pt;padding: 15px;">
                                                                <strong>Endereço:</strong>
                                                            </font>
                                                        </td>
                                                        <td>
                                                            <font style="font-family: Verdana;font-size:8pt">
                                                                <span class="valor">AV</span>
                                                                <span class="valor"> </span>
                                                                <span class="valor">DEPUTADO HUMBERTO MENDES</span>
                                                                <span class="valor"> </span>
                                                                <span class="valor">796</span>
                                                                <span class="valor"> </span>
                                                                <span class="valor">SALA 54</span>
                                                                /<span class="valor"> </span>
                                                                <span class="valor">POCO</span>
                                                                <span class="valor">  </span>
                                                                /<span class="valor">  </span>
                                                                <span class="valor">MACEIO</span>
                                                                <span class="valor"> </span>
                                                                /<span class="valor"> </span>
                                                                <span class="valor">AL</span>
                                                                <span class="valor"> / </span>
                                                                <span class="valor">57025</span>
                                                                <span class="valor">-</span>
                                                                <span class="valor">275</span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="text-align: justify;padding: 15px;">
                                                            <br>
                                                            <font style="font-family: Verdana;font-size:10pt">
                                                                A Caixa Econômica Federal, no uso da atribuição que lhe confere o Art. 7, da
                                                                Lei 8.036, de 11 de maio de 1990, certifica que, nesta data, a empresa acima identificada
                                                                encontra-se em situação regular perante o Fundo de Garantia do Tempo de Servico - FGTS.
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2"></td>
                                                    </tr>
                                                    <tr>
                                                        <td style="text-align: justify;padding: 15px;" colspan="2">
                                                            <font style="font-family: Verdana;font-size:10pt">
                                                                O presente Certificado não servirá de prova contra cobrança de quaisquer débitos referentes
                                                                a contribuições e/ou encargos devidos, decorrentes das obrigações com o FGTS.
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="padding:15px;">
                                                            <font style="font-family: Verdana;font-size:10pt">
                                                                <strong>Validade:</strong>02/11/2025 a 01/12/2025
                                                            </font>
                                                            <br><br>
                                                            <font style="font-family: Verdana;font-size:10pt">
                                                                <strong>Certificação Número: </strong>
                                                                <span class="valor">2025110205156413642881</span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td colspan="2" style="padding:15px;">
                                                            <font style="font-family:Verdana;font-size:10pt;">
                                                                <span class="valor">Informação obtida em  </span>
                                                                <span class="valor">02/11/2025 16:48:31</span>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                    <tr>
                                                        <td style="text-align:justify;padding:15px;" colspan="2">
                                                            <font style="font-family: Verdana;font-size:10pt">
                                                                A utilização deste Certificado
                                                                para os fins previstos em Lei esta condicionada a verificação de
                                                                autenticidade no site da Caixa: <strong>www.caixa.gov.br</strong>
                                                            </font>
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <input type="hidden" autocomplete="off" name="mainForm" value="mainForm">
                            <input type="hidden" autocomplete="off" name="autoScroll" value="">
                            <script type="text/javascript">
                                function clear_mainForm() {
                                    _clearJSFFormParameters('mainForm','',['mainForm:_link_hidden_','mainForm:j_idcl']);
                                }
                                function clearFormHiddenParams_mainForm(){clear_mainForm();}
                                function clearFormHiddenParams_mainForm(){clear_mainForm();}
                                clear_mainForm();
                            </script>
                            <input type="hidden" name="javax.faces.ViewState" id="_viewRoot:javax.faces.ViewState:0" value="-8851970656258686337:452040033655074486" autocomplete="off">
                        </form>
                    </div>
                </span>
            </body>
            </html>
            """,
                ]

        driver = webdriver.Chrome()
        for html_source in HTML_SOURCES:
            driver.get("data:text/html;charset=utf-8," + quote(html_source))
            extractor = CertificadoCaixaExtractor(driver=driver)
            document = extractor.run()
            #assert document.supplier.name == "BUYERS CONSULTORIA ESTRATEGICA LTDA"
            assert document.supplier.cnpj == "60.604.235/0001-14"
            assert document.document_type == "CERTIFICADO CAIXA"
            assert document.identifier == "2025110205156413642881"
            assert document.expiration_date == date(2025, 12, 1)
            