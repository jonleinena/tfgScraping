from calendar import month
import time

import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--headless")

    DRIVER = selenium.webdriver.Edge(options=chrome_options)
    return DRIVER

def get_links(DRIVER):
    links = []
    num_articles = len(DRIVER.find_elements(By.TAG_NAME, 'article')) #/html/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div/div/div[4]/article[1]
    for i in range(0, num_articles):
        links.append(DRIVER.find_element(By.XPATH,'/html/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div/div/div[4]/article[' + str(i+1)+']/div/div[1]/a').get_attribute("href"))
    links.pop(2)
    return links

def get_data(DRIVER):
    data = []
    
    data.append(DRIVER.title)
    data.append(DRIVER.find_element(By.TAG_NAME, 'section').text)
    
    
    return data

def data_to_csv(data):
    
    #f.write("name,telephone,email,website\n")
    for partner in data:
        
        f = open("./Valencia/"+str((partner[0].split("|"))[0].strip(" "))+".txt", "w")
        f.write(str((partner[0].split("|"))[0])+ "\n" + str(partner[1]))
        f.close()

if __name__ == '__main__':

    START_URL = "https://unionempresasnauticas.com/nuestros-asociados/"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        data = []
        for link in get_links(DRIVER):
            
            DRIVER.get(link)
            data.append(get_data(DRIVER))
            data_to_csv(data)
        #value = input("SCRIPT ENDED\n")
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
