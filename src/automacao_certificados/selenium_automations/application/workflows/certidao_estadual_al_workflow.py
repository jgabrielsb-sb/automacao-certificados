from automacao_certificados.selenium_automations.adapters.selenium.certidao_estadual_al.pages import *
from automacao_certificados.selenium_automations.core.models import dto_document

from pathlib import Path

class CertidaoEstadualALWorkflow:
    def __init__(
        self,
        consulta_page: ConsultaPage,
        download_page: DownloadPage,
        img_path_to_save: Path,
    ):
        self.consulta_page = consulta_page
        self.download_page = download_page
        self.img_path_to_save = img_path_to_save

    def run(
        self,
        state_value: str,
        tipo_inscricao_value: str,
        inscricao_value: str,
    ) -> tuple[dto_document.DocumentExtracted, str]:
        self.consulta_page.run(state_value, tipo_inscricao_value, inscricao_value)
        return self.download_page.run(img_path_to_save=self.img_path_to_save)