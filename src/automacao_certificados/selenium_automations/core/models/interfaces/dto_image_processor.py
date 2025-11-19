from pydantic import BaseModel

class ImageProcessorInput(BaseModel):
    base64_img: str

class ImageProcessorOutput(BaseModel):
    text: str
