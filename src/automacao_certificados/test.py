from automacao_certificados.selenium_automations.composition.container import Container
from automacao_certificados.selenium_automations.infra.api_requester import AlagoasAPIRequester, PPEAPIRequester
from automacao_certificados.selenium_automations.adapters.document_downloader import DocumentAlagoasDownloader
from automacao_certificados.selenium_automations.core.models import DocumentDownloaderInput
from automacao_certificados.config import settings

container = Container()

certidao_alagoas_downloader = DocumentAlagoasDownloader(
    api_requester=AlagoasAPIRequester(
        http=container.infrastructure.http_client
    ),
    ppe_api_requester=PPEAPIRequester(
        http=container.infrastructure.http_client,
        api_key=settings.ppe_api_key
    )
)
cnpj = '12450268000104'

if __name__ == "__main__":
    output = certidao_alagoas_downloader.run(input=DocumentDownloaderInput(cnpj=cnpj))
    print(output)