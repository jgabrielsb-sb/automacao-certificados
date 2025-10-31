import pytest
from unittest.mock import MagicMock

from selenium.webdriver.remote.webelement import WebElement
from automacao_certificados.selenium_automations.adapters.ui.selenium.utils import (
    is_img_web_element,
    get_image_as_base64,
)

class TestCheckIfWebElementIsImgElement:
    """
    Test class for the check_if_web_element_is_img_element routine.
    """

    def test_if_raises_value_error_when_web_element_is_not_a_web_element(self):
        """
        Test if the check_if_web_element_is_img_element routine raises a ValueError when the web element is not a WebElement.
        """
        with pytest.raises(ValueError):
            is_img_web_element("not_a_web_element")

    def test_if_returns_true_when_web_element_is_img(self):
        """
        Test if the check_if_web_element_is_img_element routine 
        returns True when the web element is an img element.
        """
        mock_img_web_element = MagicMock(spec=WebElement)
        mock_img_web_element.tag_name = "img"

        assert is_img_web_element(mock_img_web_element) == True

    def test_if_returns_false_when_web_element_is_not_img(self):
        """
        Test if the check_if_web_element_is_img_element routine returns False when the web element is not an img element.
        """
        mock_div_web_element = MagicMock(spec=WebElement)
        mock_div_web_element.tag_name = "div"
        
        assert is_img_web_element(mock_div_web_element) == False


class TestGetImageAsBase64:
    """
    Test class for the get_image_as_base64 routine.
    """

    def test_if_raises_value_error_when_web_element_is_not_a_web_element(self):
        """
        Test if the get_image_as_base64 routine raises a ValueError when the web element is not a WebElement.
        """
        with pytest.raises(ValueError):
            get_image_as_base64("not_a_web_element")

    def test_if_raises_value_error_when_web_element_is_not_an_img_element(self):
        """
        Test if the get_image_as_base64 routine raises a ValueError when the web element is not an img element.
        """
        with pytest.raises(ValueError):
            div_web_element = MagicMock(spec=WebElement)
            div_web_element.tag_name = "div"
            
            get_image_as_base64(div_web_element)

    def test_if_returns_the_image_as_base_64(self):
        """
        Test if the get_image_as_base64 routine returns the image as a base64 string.
        """
        mock_img_web_element = MagicMock(spec=WebElement)
        mock_img_web_element.tag_name = "img"
        mock_img_web_element.get_attribute = MagicMock(return_value="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...")
        assert get_image_as_base64(mock_img_web_element) == "iVBORw0KGgoAAAANSUhEUgAA..."