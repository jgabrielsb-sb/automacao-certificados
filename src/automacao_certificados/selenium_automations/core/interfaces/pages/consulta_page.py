from typing import Protocol, Optional

from pydantic import BaseModel

class ConsultaInput(BaseModel):
    cnpj: str
    state_value: Optional[str]

class ConsultaPagePort(Protocol):
    def run(self, input: ConsultaInput) -> None: ...

