from pathlib import Path

class CertidaoEstadualException(Exception):
    """
    Base Exception for all exceptions in Certidão Estadual AL.
    """
    pass

class ConsultaPageException(CertidaoEstadualException):
    """
    Exception for all exceptions in Consulta Page.
    """
    pass

class InvalidTipoInscricaoException(ConsultaPageException):
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

class InvalidEstadoException(ConsultaPageException):
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

class InvalidCaptchaException(ConsultaPageException):
    """
    Exception for the invalid captcha.
    """
    def __init__(
        self,
    ):
        super().__init__(
            f"Invalid captcha error: the captcha value is not correct."
        )

class IncorrectCNPJException(ConsultaPageException):
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

class NotBasicCNPJException(ConsultaPageException):
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

class NotFoundOnUFException(ConsultaPageException):
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

class DownloadPageException(CertidaoEstadualException):
    """
    Exception for all exceptions in Download Page.
    """
    pass

class ImgPathException(DownloadPageException):
    """
    Exception for the img path.
    """
    def __init__(
        self,
        message: str,
    ):
        super().__init__(message)

class ImgPathAlreadyExistsException(ImgPathException):
    """
    Exception for the img path already exists.
    """
    def __init__(
        self,
        img_path: Path,
    ):
        if not isinstance(img_path, Path):
            raise ValueError("img_path must be a Path object")
        
        super().__init__(f"The file already exists: {img_path}")






