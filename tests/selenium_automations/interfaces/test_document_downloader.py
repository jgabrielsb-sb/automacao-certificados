
import pytest

from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.models import *

@pytest.fixture
def document_downloader_implementation():
    class DocumentDownloaderImplementation(DocumentDownloaderPort):
        def _get_document(self, input: DocumentDownloaderInput):
            return "test"

    return DocumentDownloaderImplementation()

class TestDocumentDownloader:
    def test_if_all_exceptions_are_being_wrapped_into_document_downloader_exception(
        self,
        monkeypatch,
        document_downloader_implementation
    ):
        def fake_get_document(input: DocumentDownloaderInput):
            raise Exception('test exception')

        monkeypatch.setattr(
            document_downloader_implementation,
            "_get_document",
            fake_get_document
        )

        with pytest.raises(DocumentDownloaderException) as e:
            document_downloader_implementation.run(DocumentDownloaderInput(cnpj='12345678912345'))

        assert 'test exception' in str(e.value)


    