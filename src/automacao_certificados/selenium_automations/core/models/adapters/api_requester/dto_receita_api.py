
from pydantic import BaseModel

from typing import Optional

class ReceitaAPIGetCompanyResponse(BaseModel):
    CNPJ: Optional[str] = None  
    NOME_EMPRESARIAL: Optional[str] = None
    NOME_FANTASIA: Optional[str] = None
    SIT_CADASTAL: Optional[str] = None
    MOT_SIT_CADASTAL: Optional[str] = None
    DT_SIT_CADASTAL: Optional[int] = None
    DT_ABERTURA_ESTAB: Optional[int] = None
    CNAE_PRINCIPAL_COD: Optional[str] = None
    END_UF: Optional[str] = None
    OPCAO_MEI: Optional[str] = None
    PORTE: Optional[str] = None
    LISTA_QSA_SOCIO_NOME: Optional[str] = None
    END_TIPO_LOGRADOURO: Optional[str] = None
    END_LOGRADOURO: Optional[str] = None
    END_NUMERO: Optional[str] = None
    END_COMPLEMENTO: Optional[str] = None   
    END_BAIRRO: Optional[str] = None
    END_CEP: Optional[str] = None
    END_MUNICIPIO: Optional[str] = None
    DDD1: Optional[str] = None
    TELEFONE1: Optional[str] = None
    DDD2: Optional[str] = None
    TELEFONE2: Optional[str] = None
    EMAIL: Optional[str] = None
    RESPONSAVEL_CPF: Optional[str] = None
    RESPONSAVEL_NOME: Optional[str] = None
    HASH: Optional[str] = None