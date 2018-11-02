from bs4 import BeautifulSoup
import pandas as pd
import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import random
import time

# ===================================================================
#           FIND MORE BUTTON
# ===================================================================
def find(driver):
    element = driver.find_element_by_class_name('more')
    if element:
        return element
    else:
        return False


# ===================================================================
#        PARSE AND RETURN MATRIX OF COMPANIES
# ===================================================================
def parse_companies(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    tr_array = soup.find_all('div', attrs={"class": " dc59 frw44 _a _jm"})
    matrix = []
    
    for td in tr_array:
        column = []
        more_info_col = []
        column_content = td.find_all('div', attrs={"class": "base startup"})

        for item in column_content:
            # startup element to get name
            startup = item.find('div', attrs={"class": "name"}).find('a')
            more_info_col.append(startup.text.replace("\n", ""))
            more_info_col.append(startup.get('href'))

            # link to startup info itself
            pitch = item.find('div', attrs={"class", "pitch"}).text.replace("\n", "")
            more_info_col.append(pitch)
        for item in column_content:
            values = item.find_all('div', attrs={"class": "value"})
            for value in values:
                column.append(str(value.text).replace("\n", ""))
        if len(column) > 0:
            column = more_info_col + column[1:]
            matrix.append(column)
    return matrix

# ===================================================================
#        GET THE ACTUAL PAGE NUMBER TO THEN KILL THE BOT AT 20
# ===================================================================
def get_more_button_max(driver):
    soup = BeautifulSoup(driver.page_source, "html.parser")
    more_button = soup.find('div', attrs={"class": "more"})
    return int(more_button.get('data-page'))


# ===================================================================
#        save csv file
# ===================================================================
def save_dataframe(matrix):
    path = str(os.getcwd()).replace("data_collectors", "")
    directory_save = "{}datasets/angelco/".format(path)
    file_name = "angelco_companies.csv"
    columns = ["Company", "Link", "Pitch", "Joined", "Location", "Market", "Website", "Employees", "Stage", "Total_raised"]
    df = pd.DataFrame(matrix, columns=columns)
    df.to_csv("{}/{}".format(directory_save, file_name))
    df = None
    print("Dataframe saved")


# ===================================================================
#        Main Function
# ===================================================================
def main():
    driver = webdriver.Chrome("{}/chromedriver".format(os.getcwd()))
    url = "https://angel.co/companies"
    driver.get(url)
    more_button = None
    matrix = []
    parsing = True
    iterations = 0

    while parsing:
        more_button = WebDriverWait(driver, 15).until(find)
        try:
            new_matrix = parse_companies(driver)
            matrix = matrix + new_matrix
            iterations += 1

            if iterations == 10:
                save_dataframe(matrix)
                iterations = 0
            time.sleep(random.uniform(3.5, 6.9))
            more_button.click()

            if get_more_button_max(driver) == 20:
                save_dataframe(matrix)
                break
        except:
            continue
    driver.close()


if __name__=="__main__":
    main()