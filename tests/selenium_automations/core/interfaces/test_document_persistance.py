
import pytest

from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *

@pytest.fixture
def document_persistance_implementation():
    class DocumentPersistanceImplementation(DocumentPersistancePort):
        def _save(self, input: DocumentPersistanceInput):
            return "test"

    return DocumentPersistanceImplementation()

class TestDocumentPersistance:
    def test_if_all_exceptions_are_being_wrapped_into_document_persistance_exception(
        self,
        monkeypatch,
        document_persistance_implementation
    ):
        def fake_save(input: DocumentPersistanceInput):
            raise Exception('test exception')

        monkeypatch.setattr(
            document_persistance_implementation,
            "_save",
            fake_save
        )

        with pytest.raises(DocumentPersistanceException) as e:
            document_persistance_implementation.run(DocumentPersistanceInput(
                document_extracted=DocumentExtracted(
                    supplier=Supplier(cnpj='12345678912345'),
                    document_type='CERTIFICADO TEST',
                    identifier='test',
                    expiration_date=date(2025, 1, 1)
                ),
                base64_pdf='test'
            ))

        assert 'test exception' in str(e.value)


    