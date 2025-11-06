from .base_page import BasePage
from .base_image_processor import BaseImageProcessor
from .base_document_extractor import BaseDocumentExtractor
from .base_api_requester import BaseAPIRequester
from .http_client import HttpClient
from .document_acquisition import (
    DocumentAcquisitionPort, 
    DocumentRequest,
    DocumentResult
)

from .document_persistance import (
    DocumentPersistancePort,
    DocumentPersist,
    DocumentPersistResult
)