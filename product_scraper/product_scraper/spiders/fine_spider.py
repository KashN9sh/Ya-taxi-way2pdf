import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dateutil import parser

class Fine:
    date: datetime.date
    time:datetime.time
    decree: int
    cost: int

def parse_info(gos_reg, region, registration):
    fines_array = []
    fines_url = f'https://гибдд.рф/check/fines' \
                f'#{gos_reg}+{region}+{registration}'

    driver = webdriver.Safari()

    def check_exists_by_xpath(xpath):
        try:
            driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return False
        return True

    driver.get(fines_url)

    button = driver.find_element_by_xpath("//a[@class='checker']")
    button.click()

    time.sleep(3)

    if check_exists_by_xpath("//button[@class='close_modal_window']"):
        button = driver.find_element_by_xpath("//button[@class='close_modal_window']")
        button.click()
        time.sleep(3)

    fines_count = len(driver.find_elements_by_xpath("//div[@class='checkResult']/ul[@class='finesItem']"))

    for i in range(fines_count - 1):
        current_fine =  Fine
        date_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                             "ul[@class='finesItem']/li/span[@class='field fine-datedecis']")[i].text
        decree_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                             "ul[@class='finesItem']/li/span[@class='field fine-datepost']")[i].text
        cost_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                               "ul[@class='finesItem']/li/span[@class='field fine-summa']")[i].text

        current_fine.date = parser.parse(date_str.split()[0])
        current_fine.time = parser.parse(date_str.split()[2])
        current_fine.decree = decree_str.split()[0]
        current_fine.cost = cost_str.split()[0]

        fines_array.append(current_fine)

    driver.close()

     return fines_array


parse_info('У468ВХ', '797', '9931918970')
