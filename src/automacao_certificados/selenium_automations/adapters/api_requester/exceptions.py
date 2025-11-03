class APIRequesterException(Exception):
    pass

class ConflictError(APIRequesterException):
    def __init__(
        self, 
        route: str,
        object: str,
        resource_name: str,
        resource_value: str
    ) -> None:
        message = f"Object {object} already exists with {resource_name}:{resource_value}"
        super().__init__(message)

        self.route = route
        self.object = object
        self.resource_name = resource_name
        self.resource_value = resource_value

class RouteNotFoundError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str
    ) -> None:
        message = f"Route {route} not found. Please check if the route is correct."
        super().__init__(message)
        self.route = route
        self.message = message

class NotFoundError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str
    ):
        message = f"Route {route} error: {message}"
        super().__init__(message)
        self.route = route
        self.message = message

class BadRequestError(APIRequesterException):
    def __init__(
        self,
        route: str,
        message: str
    ) -> None:
        message = f"Bad request: {message}"
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
        message = f"Unexpected error: {message}"
        super().__init__(message)

        self.route = route
        self.message = message
        self.status_code = status_code