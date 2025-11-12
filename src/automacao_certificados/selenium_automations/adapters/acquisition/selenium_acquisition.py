from automacao_certificados.selenium_automations.core.interfaces import (
    DocumentAcquisitionPort,
    DocumentRequest,
    DocumentResult
)

from selenium.webdriver.remote.webdriver import WebDriver

class SeleniumAcquisition(DocumentAcquisitionPort):
    def __init__(
        self,
        webdriver: WebDriver,
        selenium_workflow,
    ):
        self.webdriver = webdriver
        self.selenium_workflow = selenium_workflow

    def acquire(self, req: DocumentRequest) -> DocumentResult:
        selenium_result = self.selenium_workflow.run(req)

        







        

