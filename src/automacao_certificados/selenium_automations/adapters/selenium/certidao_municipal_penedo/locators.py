from selenium.webdriver.common.by import By


class Locators:
    # Initial page - Certidão Negativa button in menu
    BTN_CERTIDAO_NEGATIVA_LOCATOR = (
        By.XPATH,
        "//img[contains(@src, 'bt_certidao_negativa')]"
    )

    # Imobiliário link
    LINK_IMOBILIARIO_LOCATOR = (
        By.XPATH,
        "//a[contains(text(), 'Imobiliário')]"
    )

    # Certidão Negativa span
    SPAN_CERTIDAO_NEGATIVA_LOCATOR = (
        By.XPATH,
        "//span[contains(text(), 'Certidão Negativa')]"
    )

    # CPF/CNPJ radio button
    RADIO_CPF_CNPJ_LOCATOR = (
        By.XPATH,
        "//label[contains(text(), 'CPF/CNPJ')]/parent::td/child::input"
    )

    # CNPJ input field
    INPUT_CNPJ_LOCATOR = (
        By.XPATH,
        "//input[contains(@id, 'cpfcnpjImob')]"
    )

    # Captcha image
    IMAGE_CAPTCHA_LOCATOR = (
        By.XPATH,
        "//img[contains(@id, 'Captcha')]"
    )

    # Captcha input field
    INPUT_CAPTCHA_LOCATOR = (
        By.XPATH,
        "//input[contains(@id, 'captcha')]"
    )

    # Entrar button
    BTN_ENTRAR_LOCATOR = (
        By.XPATH,
        "//span[contains(text(), 'ENTRAR')]"
    )

    # Imprimir button
    BTN_IMPRIMIR_LOCATOR = (
        By.XPATH,
        "//img[contains(@title, 'Imprimir Certidão Negativa')]"
    )

    # Error message locator (if needed)
    ERROR_MESSAGE_LOCATOR = (
        By.XPATH,
        "//span[contains(@class, 'ui-message') or contains(@class, 'error')]"
    )

locators = Locators()
