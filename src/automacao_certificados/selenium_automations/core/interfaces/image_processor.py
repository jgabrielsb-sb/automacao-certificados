from typing import Protocol, runtime_checkable

from pydantic import BaseModel

@runtime_checkable
class ImageProcessorPort(Protocol):
    """
    Image processors protocol.
    An image processor is a class that can process an image and return the text 
    from the image.
    """
    def get_text(self, base64_img: str) -> str: ...
    