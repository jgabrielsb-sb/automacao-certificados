
from pydantic import BaseModel

class Supplier(BaseModel):
    name: str
    cnpj: str

class SupplierCreate(Supplier):
    pass

class SupplierResponse(Supplier):
    id: int
