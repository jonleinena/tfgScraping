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
    
    elementos = DRIVER.find_elements(By.XPATH, '/html/body/div[2]/div/article/div/div[2]/div/div//*')[3:]
    
    subdata = []
    for elemento in elementos:
        
        if (elemento.tag_name != 'hr'):
            if(len(elemento.text) < 40 and len(elemento.text) > 1 and elemento.text not in subdata) : subdata.append(elemento.text)
        else:
            data.append(subdata)
            
            subdata = []
    
    return data

def data_to_csv(data):
    f = open("denia-partners.csv", "w")
    #f.write("name,telephone,email,website\n")
    for partner in data:
        
        
        f.write((str(partner)+"\n").replace('[', '').replace(']', ''))
    f.close()

if __name__ == '__main__':

    START_URL = "https://salonnauticodenia.com/te-ayudamos-a-exponer/lista-expositores/"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        data_to_csv(get_data(DRIVER))
        
        #value = input("SCRIPT ENDED\n")
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
