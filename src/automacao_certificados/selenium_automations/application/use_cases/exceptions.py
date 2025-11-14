class UseCaseException(Exception):
    """
    Base exception for the use cases.
    """
    pass

class DownloadCertidaoEstadualAlException(UseCaseException):
    """
    Exception for the download certidao estadual al.
    """
    def __init__(
        self,
        original_exception: Exception,
    ):
        self.original_exception = original_exception
        self.message = f"Error downloading certidao estadual al: {original_exception}"
        super().__init__(self.message)

class DownloadCertificadoMaceioException(UseCaseException):
    """
    Exception for the download certificado maceio.
    """
    def __init__(
        self,
        original_exception: Exception,
    ):
        self.original_exception = original_exception
        self.message = f"Error downloading certificado maceio: {original_exception}"
        super().__init__(self.message)

class DownloadCertificadoArapiracaException(UseCaseException):
    """
    Exception for the download certificado arapiraca.
    """
    def __init__(
        self,
        original_exception: Exception,
    ):
        self.original_exception = original_exception
        self.message = f"Error downloading certificado arapiraca: {original_exception}"
        super().__init__(self.message)