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
    num_articles = len(DRIVER.find_elements(By.CLASS_NAME, 'list_parent_item')) #/html/body/div[4]/div[1]/div[1]/div/div/div/div/div[3]/div/div/div/div/div[4]/article[1]
    print(num_articles)
    for i in range(0, num_articles):
        links.append(DRIVER.find_element(By.XPATH,'/html/body/app-root/div/app-home/div[2]/div[2]/div[2]/home-list/div/div/div[' + str(i+1)+ ']/home-list-exhibitor/div/div[2]/div/a').get_attribute("href"))
    print(len(links))
    return links

def get_data(DRIVER):
    time.sleep(5)
    data = []
    data_items = DRIVER.find_elements(By.XPATH, '/html/body/app-root/div/app-exhibitor/div/div[3]/div/div[2]/div[5]//*')
    data.append(DRIVER.find_element(By.XPATH, '/html/body/app-root/div/app-exhibitor/div/div[3]/div/div[2]/div[2]').text)
    
    for item in range(1, len(data_items)) :
        if('www.' in data_items[item].text or '+34' in data_items[item].text or '.com' in data_items[item].text or '.org' in data_items[item].text or '.cat' in data_items[item].text and data_items[item].text not in data_items):
            data.append(data_items[item].text)
    
    return data

def data_to_csv(data):
    
    #f.write("name,telephone,email,website\n")
    f = open("barcelona-partners.csv", "w")
    for partner in data:
        f.write((str(partner)+"\n").replace('[', '').replace(']', ''))
    f.close()

if __name__ == '__main__':

    START_URL = "https://ecatalogue.firabarcelona.com/salonautic2022/home?filter=ONLY_EXHIBITORS&lang=es_ES"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        time.sleep(10)
        
        for i in range(0, 20):
            DRIVER.execute_script(
                "document.getElementsByClassName('see_more_button')[0].click()"
            )
            time.sleep(3)
        data = []
        for link in get_links(DRIVER):
            DRIVER.get(link)
            data.append(get_data(DRIVER))
            data_to_csv(data)
        #value = input("SCRIPT ENDED\n")
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print('\a')
        print("Chrome cerrado")
