from automacao_certificados.selenium_automations.adapters.api_requester.certificado_api_requester import CertificadoAPIRequester
from automacao_certificados.selenium_automations.core.models import (
    dto_supplier,
    dto_document
)

from datetime import date

BASE_URL = "http://localhost:8000"

api_requester = CertificadoAPIRequester(
    base_url=BASE_URL
)

if __name__ == "__main__":
    document_response = api_requester.get_document(
        filter=dto_document.DocumentFilter(
            supplier_id=1,
            document_type_id=1,
            identifier="12345678912",
            expiration_date=date(2025, 12, 31)
        )
    )
    print(document_response)

   
