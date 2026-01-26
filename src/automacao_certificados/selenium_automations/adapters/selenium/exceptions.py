class SeleniumAdapterException(Exception):
    """
    Base exception for the selenium.
    """
    pass

class InvalidTipoInscricaoException(SeleniumAdapterException):
    """
    Exception for the invalid type of subscription.
    """
    def __init__(
        self,
        valid_tipo_inscricao_values: list[str],
        tipo_inscricao_value: str,

    ):
        """
        Args:
            tipo_inscricao_value: The value of the type of subscription.
        """
        if not isinstance(tipo_inscricao_value, str):
            raise ValueError("tipo_inscricao_value must be a string")
        
        super().__init__(
            f"Invalid type of subscription: {tipo_inscricao_value}. Valid values: {valid_tipo_inscricao_values}"
        )

class InvalidEstadoException(SeleniumAdapterException):
    """
    Exception for the invalid state.
    """
    def __init__(
        self,
        valid_state_values: list[str],
        state_value: str,
    ):
        """
        Args:
            state_value: The value of the state.
        """
        if not isinstance(state_value, str):
            raise ValueError("state_value must be a string")
        
        super().__init__(
            f"Invalid state: {state_value}. Valid values: {valid_state_values}"
        )

class InvalidCaptchaException(SeleniumAdapterException):
    """
    Exception for the invalid captcha.
    """
    def __init__(
        self,
    ):
        super().__init__(
            f"Invalid captcha error: the captcha value is not correct."
        )

class IncorrectCNPJException(SeleniumAdapterException):
    """
    Exception for the incorrect CNPJ.
    """
    def __init__(
        self,
        cnpj_value: str,
    ):
        if not isinstance(cnpj_value, str):
            raise ValueError("cnpj_value must be a string")
        
        super().__init__(
            f"Incorrect CNPJ error: the CNPJ {cnpj_value} is not correct."
        )

class NotBasicCNPJException(SeleniumAdapterException):
    """
    Exception for the not basic CNPJ.
    The CNPJ must be a basic CNPJ, that means that the CNPJ
    must have only the first 8 digits.
    """
    def __init__(
        self,
        cnpj_value: str,
    ):
        if not isinstance(cnpj_value, str):
            raise ValueError("cnpj_value must be a string")
        
        super().__init__(
            f"Not basic CNPJ error: the CNPJ {cnpj_value} is not a basic CNPJ. A basic CNPJ must have only the first 8 digits."
        )

class NotFoundOnUFException(SeleniumAdapterException):
    """
    Exception for the not found on UF.
    """
    def __init__(
        self,
        state_value: str,
        cnpj_value: str,
    ):
        if not isinstance(state_value, str):
            raise ValueError("state_value must be a string")
        if not isinstance(cnpj_value, str):
            raise ValueError("cnpj_value must be a string")
        
        super().__init__(
            f"Not found on UF error: the cnpj {cnpj_value} is not found on the state {state_value}."
        )

class CNPJNotFoundException(SeleniumAdapterException):
    """
    Exception for the CNPJ not found.
    """
    def __init__(
        self,
        cnpj_value: str,
    ):
        if not isinstance(cnpj_value, str):
            raise ValueError("cnpj_value must be a string")
        
        super().__init__(
            f"CNPJ not found error: the CNPJ {cnpj_value} is not found."
        )