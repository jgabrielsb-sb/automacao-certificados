
class HttpClientException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

class HttpClientSSLException(HttpClientException):
    def __init__(self, message):
        super().__init__(message)
        self.message = message