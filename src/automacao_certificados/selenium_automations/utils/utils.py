import base64

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
    if not cnpj.isdigit():
        raise ValueError("cnpj must be a number")
    if len(cnpj) != 14:
        raise ValueError("cnpj must have 14 digits")

    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def validate_document_file(base64_pdf: str) -> None:
    if not isinstance(base64_pdf, str):
        raise ValueError("base64_pdf must be a str")

    try:
        pdf_bytes = base64.b64decode(base64_pdf, validate=True)
    except Exception as e:
        raise ValueError("invalid base64 string: ", e)

    if not pdf_bytes.startswith(b"%PDF-"):
        raise ValueError("base64_pdf is not a valid pdf file: it does not contain %PDF on the beggining")
    
    if b"%%EOF" not in pdf_bytes:
        raise ValueError("base64_pdf is not a valid pdf file: it does not contains %%EOF")