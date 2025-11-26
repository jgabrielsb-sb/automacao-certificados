import base64

def validate_cnpj(cnpj: str) -> str:
    """
    Validate the CNPJ.

    :param cnpj: The CNPJ to validate.
    :type cnpj: str
    :return: The validated CNPJ.
    :rtype: str
    :raises ValueError: If the CNPJ is not a string or is not 14 digits or is not a number.
    """
    if not isinstance(cnpj, str):
        raise ValueError("cnpj must be a string")
    if not cnpj.isdigit():
        raise ValueError("cnpj must be a number")
    if len(cnpj) != 14:
        raise ValueError("cnpj must have 14 digits")
    return cnpj

def format_cnpj(cnpj: str) -> str:
    """
    Format the CNPJ to the format 00.000.000/0000-00.

    :param cnpj: The CNPJ to format.
    :type cnpj: str
    :return: The formatted CNPJ.
    :rtype: str
    :raises ValueError: If the CNPJ is not a string or is not 14 digits or is not a number.
    """
    cnpj = validate_cnpj(cnpj)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"

def validate_document_file(base64_pdf: str) -> None:
    """
    Validate the if the input is a valid base64 string and if it is a valid pdf file.

    :param base64_pdf: The document file in base64 format.
    :type base64_pdf: str
    :return: None.
    :rtype: None
    :raises ValueError: If the input is not a valid base64 string or is not a valid pdf file.
    """
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

def html_to_base64_pdf(html: str, data_uri: bool = False) -> str:
    """
    Render HTML to PDF (in memory) and return a Base64 string.
    - base_url: set this so relative image/CSS paths (e.g., ../estaticos/...) resolve correctly.
    - data_uri: if True, prefix with 'data:application/pdf;base64,' (handy for frontends).

    :param html: The HTML to render.
    :type html: str
    :param data_uri: If True, prefix with 'data:application/pdf;base64,' (handy for frontends).
    :type data_uri: bool
    :return: The PDF in base64 format.
    :rtype: str
    """
    from io import BytesIO
    from weasyprint import HTML
    import base64

    buf = BytesIO()
    HTML(string=html).write_pdf(buf)
    pdf_bytes = buf.getvalue()
    b64 = base64.b64encode(pdf_bytes).decode("ascii")
    return f"data:application/pdf;base64,{b64}" if data_uri else b64

def get_full_page_screenshot(driver):
    """
    Get the full page screenshot using the Chrome DevTools Protocol.

    :param driver: The driver.
    :type driver: WebDriver
    :return: The screenshot in base64 format.
    :rtype: str
    """
    # Use Chrome DevTools Protocol
    result = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "fromSurface": True,
        "captureBeyondViewport": True
    })
    
    return result["data"]   # this is a base64 PNG string

def png_base64_to_pdf_base64(png_base64: str) -> str:
    """
    Convert a PNG base64 string to a PDF base64 string.

    :param png_base64: The PNG base64 string.
    :type png_base64: str
    :return: The PDF base64 string.
    :rtype: str
    """
    import base64
    from io import BytesIO
    from PIL import Image
    
    # decode PNG
    png_bytes = base64.b64decode(png_base64)
    img = Image.open(BytesIO(png_bytes)).convert("RGB")  # PDF needs RGB
    
    # convert to PDF in memory
    pdf_bytes_io = BytesIO()
    img.save(pdf_bytes_io, format="PDF")
    
    # encode PDF to base64
    pdf_bytes = pdf_bytes_io.getvalue()
    return base64.b64encode(pdf_bytes).decode("utf-8")
