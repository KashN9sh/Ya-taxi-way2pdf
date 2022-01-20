import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Safari()


def check_exists_by_class(classname):
    try:
        driver.find_element_by_class_name(classname)
    except NoSuchElementException:
        return False
    return True

driver.get('https://yataxistzel.taxicrm.ru/payouts/payrolls')

elem = driver.find_element_by_name("phone")
elem.send_keys("9189644625")
elem.submit()

code = input()
elem = driver.find_element_by_name("code")
elem.send_keys(code)
elem.submit()

time.sleep(3)

driver.find_elements_by_class_name('user-select-item')[0].click()

time.sleep(5)

elem = driver.find_element_by_xpath("//input[@name='date_start']")
elem.click()
elem.send_keys(Keys.COMMAND, 'a')
elem.send_keys(Keys.BACKSPACE)
elem.send_keys('1')
elem.send_keys('0')
elem.send_keys('0')
elem.send_keys('9')
elem.send_keys('2')
elem.send_keys('0')
elem.send_keys('2')
elem.send_keys('0')

driver.find_element_by_class_name("page-content").click()

driver.find_element_by_xpath("//a[contains(@onclick, 'showTable()')]").click()

time.sleep(5)

# btn btn-outline red button-next margin-bottom-5
# for i in range(driver.find_elements_by_xpath('fa fa-download').count()):
for i in range(len(driver.find_elements_by_xpath('//tr/td/a'))):
    driver.find_elements_by_xpath('//tr/td/a/i')[i].click()
    time.sleep(2)
    try:
        driver.find_element_by_link_text("Скачать ведомость").click()
    except:
        print('ahaha')
    time.sleep(2)
#driver.find_element_by_xpath('//div[@class="modal-header"]/button').click()
