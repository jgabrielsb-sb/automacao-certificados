

from pydantic import BaseModel

from typing import Protocol

class DownloadInput(BaseModel):
    pass

class DownloadPagePort(Protocol):
    def run(self, input: DownloadInput) -> None: ...