from base import crawler_json

import json

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
            "side_image_url" : None,
            "main" : {
                "title" : None,
                "video_url" : None,
                "content" : None
            }
        }
        self.setting()
        self.get()
        self.driver.quit()

    def setting(self) -> None:
        self.driver.get("https://www.cgv.co.kr")

    def get(self) -> dict:
        iframe = self.wait.until(
            EC.presence_of_element_located((By.ID, "TopBanner"))
        )

        self.driver.switch_to.frame(iframe)

        side_url = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div > a:nth-child(1) > img"))
        ).get_attribute("src")

        self.driver.switch_to.default_content()

        main_div = self.wait.until(
            EC.visibility_of_element_located((By.ID, "ctl00_PlaceHolderContent_divMovieSelection_wrap"))
        )

        title = main_div.find_element(By.ID, "ctl00_PlaceHolderContent_AD_MOVIE_NM").text

        video_url = main_div.find_element(By.CSS_SELECTOR, "div > div > video > source").get_attribute("src")

        content = main_div.find_element(By.ID, "ctl00_PlaceHolderContent_AD_DESCRIPTION_NM").text
        

        self.data["side_image_url"] = side_url
        self.data["main"]["title"] = title
        self.data["main"]["video_url"] = video_url
        self.data["main"]["content"] = content

        
class movie_list(crawler_json):
    def __init__(self) -> None:
        super().__init__()
        self.data = {
            "list" : []
        }
        self.setting()
        self.get()
        # self.driver.quit()

    def setting(self) -> None:
        self.driver.get("http://www.cgv.co.kr/movies/?lt=1&ft=0")
        button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".btn-more-fontbold"))
        )
        button.click() 
        
    def get(self) -> dict:
        movie_info = {
            "rank" : None,
            "img_url" : None,
            "title" : None,
            "sales_rate" : None
        }

        movie_chart = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".sect-movie-chart"))
        )
        movies = movie_chart.find_elements(By.CSS_SELECTOR, "li")
        #for movie in movies:
            