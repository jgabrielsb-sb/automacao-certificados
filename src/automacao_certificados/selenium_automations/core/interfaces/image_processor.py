# from typing import Protocol, runtime_checkable

# from pydantic import BaseModel

# @runtime_checkable
# class ImageProcessorPort(Protocol):
#     """
#     Image processors protocol.
#     An image processor is a class that can process an image and return the text 
#     from the image.
#     """
#     def get_text(self, base64_img: str) -> str: ...

from abc import ABC, abstractmethod

from automacao_certificados.selenium_automations.core.models import *
from automacao_certificados.selenium_automations.core.exceptions import *

class ImageProcessorPort(ABC):
    """
    Image processor interface.
    """
    @abstractmethod
    def _get_text(self, input: ImageProcessorInput) -> ImageProcessorOutput:
        pass
    
    def run(self, input: ImageProcessorInput) -> ImageProcessorOutput:
        try:
            return self._get_text(input)
        except Exception as e:
            raise ImageProcessorException(e)