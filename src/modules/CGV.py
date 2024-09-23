from base import crawler_json

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
import os
import pandas as pd

class main_view(crawler_json):
    def __init__(self) -> None:
        super().__init__()
        self.data = {
            "side" : None,
            "main" : None
        }
        self.setting()
        self.get()
        self.driver.quit()

    def setting(self) -> None:
        self.driver.get("https://www.cgv.co.kr")
         

        