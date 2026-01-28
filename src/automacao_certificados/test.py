from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_penedo.pages.consulta_page import ConsultaPage
from automacao_certificados.selenium_automations.adapters.selenium.certidao_municipal_penedo.pages.download_page import DownloadPage

from automacao_certificados.selenium_automations.composition.container import Container
from automacao_certificados.selenium_automations.adapters.image_processor import GroqImageProcessor
import base64

if __name__ == "__main__":
    container = Container()
    
    consulta_page = ConsultaPage(
        driver=container.infrastructure.webdriver,
        image_processor=GroqImageProcessor(
            client=container.infrastructure.groq_client,
        )
    )
    download_page = DownloadPage(
        driver=container.infrastructure.webdriver,
    )
    consulta_page.run(cnpj='12243697000100')
    document_extracted, base64_pdf = download_page.run()
    
    with open('output.pdf', 'wb') as f:
        f.write(base64.b64decode(base64_pdf))
    print(document_extracted)