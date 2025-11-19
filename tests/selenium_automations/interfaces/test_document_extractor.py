import pytest

from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

@pytest.fixture
def document_extractor_implementation():
    class DocumentExtractorImplementation(DocumentExtractorPort):
        def get_supplier(self):
            raise Exception('test exception')
        def get_document_type(self):
            raise Exception('test exception')
        def get_expiration_date(self):
            raise Exception('test exception')
        def get_identifier(self):
            raise Exception('test exception')
            
    return DocumentExtractorImplementation()

class TestDocumentExtractor:
    def test_if_raises_document_extractor_exception_if_get_supplier_raises_exception(
        self,
        document_extractor_implementation
    ):
        with pytest.raises(DocumentExtractorException):
            document_extractor_implementation.run()