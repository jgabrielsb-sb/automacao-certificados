from abc import ABC, abstractmethod

class BaseImageProcessor(ABC):
    """
    Base class for image processors.
    An image processor is a class that can process an image and return the text 
    from the image.
    """
    @abstractmethod
    def _get_text_from_image(self, image_base64: str) -> str:
        """
        Gets the text from the image.
        Args:
            image_base64: The base64 encoded image.
        This method is implemented by the child classes.
        Returns:
            str: The text from the image.
        """
        pass

    def get_text_from_image(self, image_base64: str) -> str:
        """
        Gets the text from the image.
        Args:
            image_base64: The base64 encoded image.
        Returns:
            str: The text from the image.
        Raises:
            ValueError: If the image_base64 is not a string.
            ValueError: If the text returned by the child class is not a string.
        """
        if not isinstance(image_base64, str):
            raise ValueError("image_base64 must be a string")

        text = self._get_text_from_image(image_base64)

        if not isinstance(text, str):
            raise ValueError("text must be a string")

        return text