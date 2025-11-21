

class DocumentDownloaderException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class DocumentPersistanceException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class WorkflowException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class CaptchaSolverException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class DocumentExtractorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class ImageProcessorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class MunicipioGetterException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message