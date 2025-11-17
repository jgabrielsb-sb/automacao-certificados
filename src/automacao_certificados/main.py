from automacao_certificados.selenium_automations.application.use_cases import download_certificado_arapiraca
from automacao_certificados.selenium_automations.adapters.extractors import CertidaoArapiracaExtractor
if __name__ == "__main__":
    b64 = download_certificado_arapiraca(
        cnpj="12345678912345"
    )
    print('hello')
    
    