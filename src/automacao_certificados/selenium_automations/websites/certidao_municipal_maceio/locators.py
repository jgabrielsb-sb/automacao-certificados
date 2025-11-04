from selenium.webdriver.common.by import By

class Locators:
    INPUT_CNPJ_LOCATOR = (
        By.XPATH,
        '//input[@name="cadastroCodigoPesquisa"]'
    )

    BTN_EMITIR_CERTIFICADO_LOCATOR = (
        By.XPATH,
        '//input[@value="Emitir Certidão"]'
    )

locators = Locators()