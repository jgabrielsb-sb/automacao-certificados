from automacao_certificados.selenium_automations.core.interfaces import *
from automacao_certificados.selenium_automations.core.exceptions import *
from automacao_certificados.selenium_automations.core.models import *

import pytest

@pytest.fixture
def image_processor_port():
    class ImageProcessorPortImpl(ImageProcessorPort):
        def _get_text(self, input: ImageProcessorInput) -> ImageProcessorOutput:
            raise ImageProcessorException("Test error")
    return ImageProcessorPortImpl()

class TestImageProcessorPort:
    def test_if_raises_image_processor_exception_if_unexpected_error_occurs(
        self,
        image_processor_port: ImageProcessorPort,
    ):
        with pytest.raises(ImageProcessorException):
            image_processor_port.run(input=ImageProcessorInput(base64_img="test"))