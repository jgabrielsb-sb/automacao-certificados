from selenium.webdriver.common.by import By

class Locators:
    BTN_CERTIDAO_GERAL_LOCATOR = (
        By.XPATH,
        "//a[contains(text(), 'Certidão Contribuinte Geral')]"
    )

    SELECT_PESSOA_JURIDICA_LOCATOR = (
        By.XPATH, 
        "//tr[contains(@id, 'Rowselecione')]//select[contains(@name, 'PESSOATIPO')]"
    )

    INPUT_CNPJ_LOCATOR = (
        By.XPATH, 
        "//input[contains(@name, 'CNPJ')]"
    )

    CONSULTAR_BUTTON_LOCATOR = (
        By.XPATH,
        "//input[contains(@value, 'Consultar')]"
    )

    CNPJ_INVALIDO = (
        By.XPATH,
        "//b[contains(text(), 'CPF/CNPJ')]"
    )

locators = Locators()