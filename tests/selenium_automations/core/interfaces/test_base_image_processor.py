import pytest
from unittest.mock import patch

from automacao_certificados.selenium_automations.core.interfaces import BaseImageProcessor


@pytest.fixture
def image_processor_class() -> type[BaseImageProcessor]:
    """
    Fixture to create a BaseImageProcessor instance.
    """
    class MockImageProcessor(BaseImageProcessor):
        """
        Mock class for the BaseImageProcessor interface.
        """
        def _get_text_from_image(self, image_base64: str) -> str:
            return "test"

    return MockImageProcessor

class TestBaseImageProcessor:
    """
    Test class for the BaseImageProcessor interface.
    """
    def test_if_returns_the_text_from_the_image(
        self,
        image_processor_class: type[BaseImageProcessor],
    ):
        """
        Test if the BaseImageProcessor returns the text from the image.
        """
        image_processor = image_processor_class()
        assert image_processor.get_text_from_image(image_base64="hsfjlshfjdsl") == "test"

    def test_if_raises_value_error_if_text_is_not_a_string(
        self,
        image_processor_class: type[BaseImageProcessor],
    ):
        """
        Test if the BaseImageProcessor raises a ValueError if the text is not a string.
        """
       
        image_processor = image_processor_class()
        
        with patch.object(image_processor, "_get_text_from_image", return_value=123):
            with pytest.raises(ValueError):
                image_processor.get_text_from_image(image_base64="hsfjlshfjdsl")

    def test_if_raises_value_error_if_image_base64_is_not_a_string(
        self,
        image_processor_class: type[BaseImageProcessor],
    ):
        """
        Test if the BaseImageProcessor raises a ValueError if the image_base64 is not a string.
        """
        image_processor = image_processor_class()
        
        with pytest.raises(ValueError):
            image_processor.get_text_from_image(image_base64=123)