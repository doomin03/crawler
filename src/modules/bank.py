from base import crawler

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import time
import os
import pandas as pd
import openpyxl

class AddressCrawler(crawler):
    def __init__(self) -> None:
        super().__init__()
        self.data = []
        self.setting()
        self.get(page_num=139)
        self.driver.quit()
    
    def setting(self) -> None:
        self.driver.get("https://nonghyup.ttmap.co.kr/main.jsp")
        
        left_wrap = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '#left_wrap'))
        )
        
        li_element = left_wrap.find_elements(By.CSS_SELECTOR, 'div.left_container ul.btn_radio > li')[1]
        li_element.click()
        
        tabs = self.wait.until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, 'div.tab_main > ul > li'))
        )
        tabs[1].click()
        tabs[0].click()
    
    def get(self, page_num=5) -> None:
        for page_number in range(1, page_num + 1):
            try:
                self.driver.execute_script(f"javascript:goPage({page_number});")
                
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#result_list > ul'))
                )
                time.sleep(2)

                result_list = self.wait.until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, '#result_list > ul'))
                )
                lists = result_list.find_elements(By.CSS_SELECTOR, 'li.lists')
                
                
                
                for list_item in lists:
                    try:
                        title = list_item.find_element(By.CSS_SELECTOR, 'h2.list_title.nhbank').text
                        address = list_item.find_element(By.CSS_SELECTOR, 'p.list_addr').text
                        tel_num = list_item.find_element(By.CSS_SELECTOR, 'p.list_telno').text
                        
                        item = {
                            'title': title,
                            'address': address,
                            'telephone_number': tel_num
                        }
                        
                        if item not in self.data:
                            self.data.append(item)
                    
                    except (NoSuchElementException, StaleElementReferenceException) as e:
                        print(e)
                
                time.sleep(2)
            
            except TimeoutException:
                print(page_number)
                break
    
    def get_pd(self) -> pd.DataFrame:
        return pd.DataFrame(self.data)

    def save_to_excel(self, file_name: str) -> None:
        output_dir = r"C:\Users\jung3\Desktop\방학프로젝트\crawler\src\modules\output"
        os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
        file_path = os.path.join(output_dir, file_name)
        df = self.get_pd()
        df.to_excel(file_path, index=False)
        print(f"Data has been saved to {file_path}")

a = AddressCrawler()
a.save_to_excel("address_data.xlsx")
