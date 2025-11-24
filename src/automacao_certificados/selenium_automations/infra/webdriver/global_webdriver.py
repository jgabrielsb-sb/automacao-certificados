from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automacao_certificados.config import settings

HEADLESS = settings.headless

def get_options():
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument('--headless')

    return options

def get_global_webdriver():
    return webdriver.Chrome(options=get_options())

