from calendar import month
import time

import selenium
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pynput.keyboard import Key, Controller


def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    # chrome_options.add_argument("--headless")

    DRIVER = selenium.webdriver.Edge(options=chrome_options)
    return DRIVER


def login(LOGIN_PAGE: selenium.webdriver.Edge):
    username = LOGIN_PAGE.find_element(By.XPATH, '//*[@id="user_email"]')
    username.clear()
    username.send_keys("leinenajon@gmail.com")
    password = LOGIN_PAGE.find_element(By.XPATH, '//*[@id="user_password"]')
    password.clear()
    password.send_keys("Fightingalloy9*")

    time.sleep(1)
    LOGIN_PAGE.execute_script(
        "document.getElementsByClassName('icheckbox')[0].setAttribute('class' , '')")

    LOGIN_PAGE.execute_script(
        "document.getElementsByClassName('icheck-input')[0].setAttribute('class' , '')")

    LOGIN_PAGE.find_element(
        By.XPATH, '/html/body/div[5]/main/div[3]/div/div[1]/div/form/div[3]/label/div/input').click()

    LOGIN_PAGE.find_element(
        By.XPATH, '//*[@id="new_user"]/p[1]/input').send_keys("\n")

    WebDriverWait(LOGIN_PAGE, 60).until(
        EC.title_is("Grupos | Official U.S. Department of State Visa Appointment Service | Spain | Spanish"))


def goto_schedule(DRIVER: selenium.webdriver.Edge):
    DRIVER.find_element(
        By.XPATH, '//*[@id="main"]/div[2]/div[2]/div[1]/div/div/div[1]/div[2]/ul/li/a').click()

    time.sleep(2)

    DRIVER.find_element(
        By.XPATH, '/html/body/div[4]/main/div[2]/div[2]/div/section/ul/li[3]').click()
    """ DRIVER.execute_script(
        "document.getElementsByClassName('accordion-item')[2].setAttribute('class', 'accordion-item is-active')")

    DRIVER.execute_script(
        "document.getElementById('accordion-item')[2].setAttribute('class', 'accordion-item is-active')") """

    time.sleep(2)
    DRIVER.find_element(By.XPATH,
                        "//a[contains(text(), 'Reprogramar cita')]").click()


def new_dates(DRIVER: selenium.webdriver.Edge):
    time.sleep(5)
    unselectable = "ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled"

    DRIVER.find_element(
        By.XPATH, '//*[@id="appointments_consulate_appointment_date"]').click()

    found = False

    while(not found):

        tabla_first = DRIVER.find_elements(
            By.XPATH, '/html/body/div[5]/div[1]/table/tbody/tr')

        for i in range(0, 5):
            elements = tabla_first[i].find_elements(By.XPATH, "./child::*")

            for element in elements:
                if(element.get_attribute("class") != unselectable and element.get_attribute('class') == " undefined"):

                    print(str(element.get_attribute('data-month')) +
                          " - " + str(element.get_attribute('data-year')))
                    date = element.find_element(
                        By.TAG_NAME, "a").get_attribute("inner_text")
                    print(date)
                    found = True
                    break
            if(found == True):
                break
        DRIVER.find_element(
            By.XPATH, '//*[@id="ui-datepicker-div"]/div[2]/div/a').click()

    time.sleep(8)


if __name__ == '__main__':

    START_URL = "https://ais.usvisa-info.com/es-es/niv/users/sign_in"

    try:

        DRIVER = create_driver()
        DRIVER.get(START_URL)
        login(DRIVER)
        print("logged in!")
        goto_schedule(DRIVER)
        new_dates(DRIVER)
        #value = input("SCRIPT ENDED\n")
    finally:
        DRIVER.delete_all_cookies()
        DRIVER.quit()
        print("Chrome cerrado")
