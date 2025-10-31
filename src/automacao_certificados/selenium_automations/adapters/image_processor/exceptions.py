from ...core.exceptions import BaseImageProcessorException

class MissingConfigurationException(BaseImageProcessorException):
    """
    Exception for the missing configuration error.
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

class AuthenticationException(BaseImageProcessorException):
    """
    Exception for the authentication error.
    """
    def __init__(
        self,
        service_name: str,
        original_exception: Exception = None,
    ):
        """
        Args:
            service_name: The name of the service that caused the error.
            error: The error that occurred.
        """
        if not isinstance(service_name, str):
            raise ValueError("service_name must be a string")

        if original_exception:
            if not isinstance(original_exception, Exception):
                raise ValueError("original_exception must be an Exception")

        self.service_name = service_name
        self.original_exception = original_exception

        if original_exception:
            self.message = f"Authentication error for {service_name}: {original_exception}"
        else:
            self.message = f"Authentication error for {service_name}"

        super().__init__(self.message)

class InvalidParametersException(BaseImageProcessorException):
    """
    Exception for the invalid parameters error.
    """
    def __init__(
        self,
        service_name: str,
        parameter_name: str,
        parameter_value: any,
        original_exception: Exception = None,
    ):
        """
        Args:
            service_name: The name of the service that caused the error.
            parameter_name: The name of the parameter that caused the error.
            parameter_value: The value of the parameter that caused the error.
            original_exception: The original exception that occurred.
        """
        if not isinstance(service_name, str):
            raise ValueError("service_name must be a string")

        if not isinstance(parameter_name, str):
            raise ValueError("parameter_name must be a string")

        if original_exception:
            if not isinstance(original_exception, Exception):
                raise ValueError("original_exception must be an Exception")

        self.service_name = service_name
        self.parameter_name = parameter_name
        self.parameter_value = parameter_value
        self.original_exception = original_exception

        if original_exception:
            self.message = f"Invalid parameters error for {service_name}: {parameter_name} = {parameter_value}: {original_exception}"
        else:
            self.message = f"Invalid parameters error for {service_name}: {parameter_name} = {parameter_value}"
        
        super().__init__(self.message)
        
class UnexpectedImageProcessingException(BaseImageProcessorException):
    """
    Exception for the unexpected image processing error.
    """
    def __init__(
        self,
        service_name: str,
        original_exception: Exception,
    ):
        """
        Args:
            service_name: The name of the service that caused the error.
            original_exception: The original exception that occurred.
        """
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an Exception")

        if not isinstance(service_name, str):
            raise ValueError("service_name must be a string")

        self.original_exception = original_exception
        self.service_name = service_name

        super().__init__(f"Unexpected image processing error for {service_name}: {original_exception}")



    