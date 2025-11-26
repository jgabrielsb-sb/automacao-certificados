from pydantic import BaseModel

from automacao_certificados.selenium_automations.core.models import dto_document

class DocumentDownloaderInput(BaseModel):
    """
    Input model for document downloader operations.
    
    This model contains the parameters needed to download a certificate
    document from a source.
    
    Attributes:
        cnpj (str): The CNPJ (company registration number) of the company
                    whose certificate should be downloaded.
    """
    cnpj: str

class DocumentDownloaderOutput(BaseModel):
    """
    Output model for document downloader operations.
    
    This model contains the results of a document download operation,
    including the extracted document information and the PDF file.
    
    Attributes:
        document_extracted: The extracted document information. See
                           :class:`dto_document.DocumentExtracted` for details.
        base64_pdf (str): The PDF file encoded as a Base64 string.
    """
    document_extracted: dto_document.DocumentExtracted
    base64_pdf: str