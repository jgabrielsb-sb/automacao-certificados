from enum import Enum

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from automacao_certificados.config import settings

import os

HEADLESS = settings.headless

def get_options():
    options = webdriver.ChromeOptions()
    download_dir = os.path.abspath("downloads")

    prefs = {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,  # key line
    }
    
    options.add_experimental_option("prefs", prefs)
    
    if HEADLESS:
        options.add_argument('--headless')
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage") 
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        )
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    return options

def get_global_webdriver():
    return webdriver.Chrome(options=get_options())

