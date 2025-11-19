
import pytest

from automacao_certificados.selenium_automations.core.exceptions.interfaces.exceptions import DocumentDownloaderException
from automacao_certificados.selenium_automations.core.interfaces import *

@pytest.fixture
def document_downloader_implementation():
    class DocumentDownloaderImplementation(DocumentDownloaderPort):
        def get_document(self, cnpj):
            return "test"

    return DocumentDownloaderImplementation()

class TestDocumentDownloader:
    def test_if_all_exceptions_are_being_wrapped_into_document_downloader_exception(
        self,
        monkeypatch,
        document_downloader_implementation
    ):
        def fake_get_document(cnpj):
            raise Exception('test exception')

        monkeypatch.setattr(
            document_downloader_implementation,
            "get_document",
            fake_get_document
        )

        with pytest.raises(DocumentDownloaderException) as e:
            document_downloader_implementation.run('12345678912345')

        assert 'test exception' in str(e.value)


    