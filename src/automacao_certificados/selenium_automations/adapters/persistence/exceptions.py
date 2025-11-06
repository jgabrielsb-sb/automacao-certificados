

class PersistenceException(Exception):
    """
    Base exception for the persistence.
    """
    pass

class DocumentTypeNotFoundError(PersistenceException):
    """
    Exception for the document type not found error.
    """
    def __init__(
        self,
        message: str,
    ):
        """
        Args:
            message: The message of the exception.
        """
        if not isinstance(message, str):
            raise ValueError("message must be a string")

        super().__init__(message)
        self.message = message