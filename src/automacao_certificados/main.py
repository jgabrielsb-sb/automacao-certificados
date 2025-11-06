
from pathlib import Path
import base64

from automacao_certificados.selenium_automations.adapters.api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.adapters.http import HttpxClient

from automacao_certificados.selenium_automations.core.models import dto_document
from datetime import date

pdf_path = Path("tests/data/certificados/certificados_maceio/certidao_maceio_1.pdf")


if __name__ == "__main__":

    with open(pdf_path, "rb") as pdf_file:
        pdf_bytes = pdf_file.read()
        base64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

    # with open(Path("pdf_copy.pdf"), "wb") as new_pdf_file:
    #     new_pdf_file.write(pdf_bytes)

    api_requester = CertificadoAPIRequester(
        base_url="http://localhost:8000",
        http=HttpxClient()
    )

    document_create = dto_document.DocumentCreate(
        supplier_id=95,
        document_type_id=6,
        identifier="1234567912",
        expiration_date=date(2025, 12, 31),
        base64_pdf=base64_pdf
    )

    api_requester.register_document(document_create)