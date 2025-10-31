from selenium.webdriver.remote.webelement import WebElement

def is_img_web_element(
    img_web_element: WebElement,
) -> bool:
    """
    Checks if the web element is an img element: those with <img> tag-name.
    Args:
        img_web_element: The web element to check.
    Returns:
        bool: True if the web element is an img element, False otherwise.
    Raises:
        ValueError: If the web element is not a WebElement.
    """
    if not isinstance(img_web_element, WebElement):
        raise ValueError("img_web_element must be a WebElement")

    return img_web_element.tag_name == "img"

def get_image_as_base64(
    img_web_element: WebElement,
) -> str:
    """
    Gets the image as a base64 string given a img web element.
    Args:
        img_web_element: The web element that contains the image.
    Returns:
        str: The image as a base64 string.
    Raises:
        ValueError: If the web element is not a WebElement.
    """
    def _remove_prefix(src: str) -> str:
        return src.split(",", 1)[1]

    import base64

    if not isinstance(img_web_element, WebElement):
        raise ValueError("img_web_element must be a WebElement")

    if not is_img_web_element(img_web_element):
        raise ValueError("img_web_element must be an img element")
    
    src = img_web_element.get_attribute("src")
    base64_img = _remove_prefix(src)
    return base64_img
    