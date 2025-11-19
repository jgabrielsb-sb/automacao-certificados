class ExtractorException(Exception):
    """
    Base exception for the extractors.
    """
    pass

class ErrorExtractingDataException(ExtractorException):
    """
    Exception for the error extracting data.
    """
    def __init__(
        self,
        field_name: str,
        original_exception: Exception = None,
    ):
        """
        Args:
            field_name: The name of the field that caused the error.
            original_exception: The original exception that occurred.
        """
        if not isinstance(field_name, str):
            raise ValueError("field_name must be a string")

        if original_exception:
            if not isinstance(original_exception, Exception):
                raise ValueError("original_exception must be an Exception")

        self.field_name = field_name
        self.original_exception = original_exception

        if original_exception:
            self.message = f"Error extracting data for {field_name}: {original_exception}"
        else:
            self.message = f"Error extracting data for {field_name}"

        super().__init__(self.message)