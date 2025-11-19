from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

HEADLESS = False

def get_options():
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument('--headless')

    return options

def get_global_webdriver():
    return webdriver.Chrome(options=get_options())

