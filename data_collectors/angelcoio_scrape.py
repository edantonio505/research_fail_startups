from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
import time





def main():
    driver = webdriver.Chrome("{}/chromedriver".format(os.getcwd()))
    url = "https://angel.co/companies"
    driver.get(url)
    more_button = None
    try:
        more_button = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "more"))
        )
        time.sleep(random.uniform(3.5, 6.9))
        more_button.click()
        time.sleep(random.uniform(3.5, 6.9))

        soup = BeautifulSoup(driver.page_source, "html.parser")

        print(soup.prettify())



    except Exception as e:
        print("Error occurred: {}".format(e))
        driver.quit()










    driver.close()











if __name__=="__main__":
    main()