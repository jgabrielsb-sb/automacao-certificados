class EmailException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmailConnectionException(EmailException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmailTLSConnectionException(EmailException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmailLoginException(EmailException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class EmailSendException(EmailException):
    def __init__(self, message):
        super().__init__()
        self.message = message

