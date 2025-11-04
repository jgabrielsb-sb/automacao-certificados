

def format_cnpj(cnpj: str) -> str:
    """
    Format the CNPJ to the format 00.000.000/0000-00.
    Arguments:
        cnpj: str - The CNPJ to format.
    Returns:
        str - The formatted CNPJ.
    Raises:
        ValueError: If the CNPJ is not a string or is not 14 digits or is not a number.
    """
    if not isinstance(cnpj, str):
        raise ValueError("cnpj must be a string")
    if len(cnpj) != 14:
        raise ValueError("cnpj must be 14 digits")
    if not cnpj.isdigit():
        raise ValueError("cnpj must be a number")

    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"