import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


def parse_info(gos_reg, region, registration):
    params = {
        'number': gos_reg,
        'region': region,
        'registration': registration
    }

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
        date = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                             "ul[@class='finesItem']/li/span[@class='field fine-datedecis']")[i].text
        decree = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                             "ul[@class='finesItem']/li/span[@class='field fine-datepost']")[i].text
        cost = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                               "ul[@class='finesItem']/li/span[@class='field fine-summa']")[i].text

        print(date)
        print(decree)
        print(cost)

    driver.close()

    # return item


parse_info('У468ВХ', '797', '9931918970')
