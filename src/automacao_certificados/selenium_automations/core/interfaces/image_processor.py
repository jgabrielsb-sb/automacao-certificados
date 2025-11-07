from typing import Protocol

from pydantic import BaseModel

class ImageProcessorPort(Protocol):
    """
    Image processors protocol.
    An image processor is a class that can process an image and return the text 
    from the image.
    """
    def get_text(self, base64_img: str) -> str: ...
    