from selenium.webdriver.common.by import By


class Locators:
    CAPTCHA_INPUT_LOCATOR = (
        By.XPATH,
        '//div[@class="captcha-texto"]/input'
    )

    CAPTCHA_IMAGE_LOCATOR = (
        By.XPATH,
        '//div[@class="captcha-imagem"]/img'
    )

    INPUT_INSCRICAO = (
        By.XPATH,
        '//label[contains(text(), "Inscrição")]/following-sibling::input'
    )

    SELECT_TIPO_INSCRICAO = (
        By.XPATH,
        '//label[contains(text(), "Inscrição")]/parent::div//select'
    )

    SELECT_TIPO_INSCRICAO_LABEL = (
        By.XPATH,
        '//label[contains(text(), "Inscrição")]/parent::div//span[@class="select-label"]'
    )

    SELECT_ESTADO = (
        By.XPATH,
        '//label[contains(text(), "UF")]/parent::div//select'
    )

    SELECT_ESTADO_LABEL = (
        By.XPATH,
        '//label[contains(text(), "UF")]/parent::div//span[@class="select-label"]'
    )

    CONSULTAR_BUTTON = (
        By.XPATH,
        '//input[@value="Consultar"]'
    )

    ERROR_TEXT = (
        By.XPATH,
        '//span[@class="feedback-text"]'
    )

    TABLE_LOCATOR = (
        By.XPATH,
        '//table'
    )

    ROW_LOCATOR = (
        By.XPATH,
        '//tbody/tr'
    )

    COLUMNS_LOCATOR = (
        By.XPATH,
        './/td'
    )

    CERTIFICADO_HREF_LOCATOR = (
        By.XPATH,
        '//a[contains(text(), "Certificado")]'
    )

    VISUALIZAR_BUTTON_LOCATOR = (
        By.XPATH,
        '//input[@value="Visualizar"]'
    )

    CERTIFICADO_TABLE_LOCATOR = (
        By.XPATH,
        '//table[contains(., "Certificado")]'
    )

locators = Locators()