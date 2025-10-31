class CaptchaException(Exception):
    """
    Base exception for the captcha solver.
    """
    pass

class NotSupportedAdapterException(CaptchaException):
    """
    Exception for the not supported adapter error.
    """
    def __init__(
        self,
        adapter_value: str,
    ):
        """
        Args:
            adapter_value: The value of the adapter.
        """ 
        if not isinstance(adapter_value, str):
            raise ValueError("adapter_value must be a string")
            
        message = f"Adapter {adapter_value} is not supported"
        super().__init__(message)


class MissingConfigurationException(CaptchaException):
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

        self.message = message
        super().__init__(message)

class UnexpectedCaptchaException(CaptchaException):
    """
    Exception for the unexpected captcha solver error.
    """
    def __init__(
        self,
        original_exception: Exception,
    ):
        """
        Args:
            original_exception: The original exception that occurred.
        """
        
        if not isinstance(original_exception, Exception):
            raise ValueError("original_exception must be an Exception")

        self.original_exception = original_exception
        super().__init__(f"Unexpected captcha solver error: {original_exception}")

