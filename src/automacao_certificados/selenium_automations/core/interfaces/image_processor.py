from typing import Protocol

from pydantic import BaseModel

class ImageProcessorInput(BaseModel):
    """
    The input is the encoded base 64 string.
    """
    base64_img: str

class ImageProcessorOutput(BaseModel):
    """
    The output is the text on the image.
    """
    text: str


class ImageProcessorPort(Protocol):
    """
    Image processors protocol.
    An image processor is a class that can process an image and return the text 
    from the image.
    """
    def get_text(self, input: ImageProcessorInput) -> ImageProcessorOutput: ...
    