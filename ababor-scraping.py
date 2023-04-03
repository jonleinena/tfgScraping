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

def get_data(DRIVER):
    data = []
    columns = DRIVER.find_elements(By.CLASS_NAME, 'columns') #//*[@id="catalogo-ancho"]/div/div/div/div[2]/div/div[1]/div[1]/div/text()
    for column in columns:
        contact_info = column.find_element(By.CLASS_NAME, 'datos-contacto')
        text_csv = (contact_info.text).split("\n")
        if(len(text_csv)<4): text_csv.append('')
        data.append(text_csv)
        #data[contact_info.text] = contact_info.find_element(By.XPATH, '//div/div/div/div[2]/div/div[1]/div[1]/div/a[3]').text
    return data

def data_to_csv(data):
    f = open("partners.csv", "w")
    f.write("name,telephone,email,website\n")
    for partner in data:
        f.write(str(partner[0])+","+str(partner[1])+","+str(partner[2])+","+str(partner[3])+"\n")
    f.close()

if __name__ == '__main__':

    START_URL = "https://www.ababor.eus/expositores/catalogo-expositores-ababor-2023/"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        
        data_to_csv(get_data(DRIVER))
        #value = input("SCRIPT ENDED\n")
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
