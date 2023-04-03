import numpy as np
import re
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


def get_uniques(filename):
    f = open(filename, 'r')
    data = []
    line = f.readline()
    
    while(line != ""):
        #split_data = list(np.unique(np.array(line.strip('\n').split(','))))
        split_data = line.strip('\n').split(',')
        clean_data = []
        for elem in split_data:  
            if(elem not in clean_data): clean_data.append(elem)
        if(clean_data not in data) : data.append(clean_data)
        line = f.readline()
    f.close()
    return data

def write_file(filename, data):
    f = open(filename, 'w')
    for element in data:
        f.write((str(element)+"\n").replace('[', '').replace(']', '').replace('"', ""))
    f.close()

def get_websites(data): #se podria hacer con un diccionario
    websites = []
    for element in data:
        website = list(filter(lambda x: ('www.' or  ".org" or  ".cat" or  ".com") in x, element))
        if len(website) > 0: website[0] = "".join(website[0].split()).replace("'", "")
        #print(website) 
        websites.append(website)
    #print(websites)
    return(websites)



def get_emails(DRIVER, websites, REGEX):
    
    for web in websites:
        if(len(web) > 0):    
            try: 
                DRIVER.get("https://"+str(web[0]))
                page_source = DRIVER.page_source
                for re_match in re.finditer(REGEX, page_source):
                    if(str(re_match.group()) not in web) : web.append(str(re_match.group()))
            except:
                print("no se pudo obtener la web: "+ str(web[0]))
        else:
            websites.remove(web)
    return websites

def append_emails(partner_data, emails_list):
    index = 0
    for element in partner_data:
        element.append(emails_list[index][1:])
        index +=1
    return partner_data



if __name__ == '__main__':
    ORIGINAL_FILE = 'barcelona-partners.csv'
    FILE_NAME = 'bcn-partners(2).csv'
    REGEX = re.compile("(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"+"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*"+")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])")
    try:
        DRIVER = create_driver()
        uniques = get_uniques(ORIGINAL_FILE)
        webs = get_websites(uniques)
        emails = get_emails(DRIVER, webs, REGEX)
        
        write_file(FILE_NAME, append_emails(uniques, emails))
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print('\a')
        print('Edge Cerrado')