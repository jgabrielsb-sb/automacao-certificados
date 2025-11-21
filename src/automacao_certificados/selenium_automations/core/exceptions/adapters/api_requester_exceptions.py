class APIRequesterException(Exception):
    pass

class ConflictError(APIRequesterException):
    def __init__(
        self, 
        route: str,
        message: str
    ) -> None:
        super().__init__(message)
        self.route = route
        self.message = message

class RouteNotFoundError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str,
    ) -> None:
        super().__init__(message)
        self.route = route
        self.message = message

class NotFoundError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str,
    ):
        super().__init__(message)
        self.route = route
        self.message = message
        
class BadRequestError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str
    ) -> None:
        super().__init__(message)
        self.route = route
        self.message = message

class UnexpectedError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str,
        status_code: str,
    ) -> None:
        super().__init__(message)
        self.route = route
        self.status_code = status_code
        self.message = message

class InvalidCNPJException(APIRequesterException):
    def __init__(
        self,
        cnpj: str,
        custom_message: str = None
    ) -> None:
        self.cnpj = cnpj

        if not custom_message:
            custom_message = f"CNPJ inválido: {cnpj}"

        self.message = custom_message
        super().__init__(self.message)

class InternalServerError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str,
        status_code: str,
    ) -> None:
        super().__init__(message)
        self.route = route
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f"Internal Server Error: {self.message} - Route: {self.route} - Status Code: {self.status_code}"