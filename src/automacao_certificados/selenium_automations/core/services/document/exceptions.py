

class DocumentServiceError(Exception):
    """
    Exception raised when an error occurs in the document service.
    """
    pass

class DocumentTypeNotFoundError(DocumentServiceError):
    """
    Exception raised when a document type is not found.
    """
    def __init__(
        self,
        message: str
    ):
        self.message = message
        super().__init__(self.message)