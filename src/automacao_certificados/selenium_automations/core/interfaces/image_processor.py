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
    Interface responsible for defining the contract for image processors.
    """
    @abstractmethod
    def get_text(self, input: ImageProcessorInput) -> ImageProcessorOutput:
        """
        Gets the text from the image.
        
        :param input: the input of the image processor.
        :type input: ImageProcessorInput
        :return: the output of the image processor.
        :rtype: ImageProcessorOutput
        """
        pass
    
    def run(self, input: ImageProcessorInput) -> ImageProcessorOutput:
        """
        Runs the image processor.
        
        :param input: the input of the image processor.
        :type input: ImageProcessorInput
        :return: the output of the image processor.
        :rtype: ImageProcessorOutput
        """
        try:
            return self.get_text(input)
        except Exception as e:
            raise ImageProcessorException(e)