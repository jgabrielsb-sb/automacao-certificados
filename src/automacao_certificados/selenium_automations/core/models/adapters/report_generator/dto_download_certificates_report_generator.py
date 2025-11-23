
from pydantic import BaseModel, ConfigDict

class DownloadCertificatesRow(BaseModel):
    cnpj: str
    document_type: str
    error_selection: str | None = None

    download_step_is_sucess: bool
    download_step_error_message: str | None = None

    persistance_step_is_sucess: bool
    persistance_step_error_message: str | None = None

    ppe_step_is_sucess: bool
    ppe_step_error_message: str | None = None

class DownloadCertificatesTable(BaseModel):
    rows: list[DownloadCertificatesRow]

    model_config = ConfigDict(arbitrary_types_allowed=True)
    
