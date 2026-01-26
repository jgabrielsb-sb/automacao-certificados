from selenium.webdriver.common.by import By


class Locators:
    SELECT_TIPO_CONSULTA = (
        By.XPATH,
        "//*[@id='tipoConsulta']"
    )

    INPUT_TIPO_CONSULTA_ECONOMICO = (
        By.XPATH,
        '//*[@ng-model="tipoConsultaEconomico" and @value="2"]'
    )

    INPUT_CNPJ = (
        By.XPATH,
        '//*[@id="cnpjCertidoes"]'
    )

    SELECT_TIPO_CERTIDAO = (
        By.XPATH,
        '//*[@id="tipoCertidao"]'
    )

    BUTTON_IMPRIMIR = (
        By.XPATH,
        '//*[@id="btnImprimirCertidaoDebitos"]'
    )

    RADIO_NOVA_CERTIDAO = (
        By.XPATH,
        '//*[@id="radNovaCertidao"]'
    )

    BUTTON_CONTINUAR = (
        By.XPATH,
        '//*[@id="windowOpcaoImpressao"]/div/div/div[3]/button[1]'
    )

    CERTIFICADO_IMAGE_LOCATOR = (
        By.XPATH,
        '//*[@id="MvcViewerReportPanel"]/div'
    )

locators = Locators()
