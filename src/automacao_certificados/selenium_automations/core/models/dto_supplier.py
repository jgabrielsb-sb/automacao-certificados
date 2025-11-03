
from pydantic import BaseModel

class Supplier(BaseModel):
    cnpj: str

class SupplierCreate(Supplier):
    pass

class SupplierResponse(Supplier):
    id: int
