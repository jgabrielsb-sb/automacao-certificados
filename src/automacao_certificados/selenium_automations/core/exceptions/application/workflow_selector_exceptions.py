class WorkflowSelectorException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class MunicipioNotSupportedException(WorkflowSelectorException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class DocumentTypeNotSupportedException(WorkflowSelectorException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
