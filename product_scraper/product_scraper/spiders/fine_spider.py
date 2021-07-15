import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from dateutil import parser
import datetime
import requests


class Fine:
    date: datetime.date
    time: datetime.time
    decree: int
    cost: int

def get_shtruls_from_api():
    url_auth = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'

    headers = {
        'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
        'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
    }

    shtrul_array = []

    data = {"query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f",
                               "driver_profile": {"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe",
                                                                   "badd1c9d6b6b4e9fb9e0b48367850467"],
                                                  "work_status": ["working", "not_working"]}}}}
    response = requests.post(url_auth, headers=headers, json=data)

    car_number = []
    region = []
    sts = []

    for i in range(len(response.json()['driver_profiles'])):
        if 'car' in response.json()['driver_profiles'][i]:
            car_number.append(response.json()['driver_profiles'][i]['car']['number'][0:6])
            region.append(response.json()['driver_profiles'][i]['car']['number'][6:])
            if 'registration_cert' in response.json()['driver_profiles'][i]['car']:
                sts.append(response.json()['driver_profiles'][i]['car']['registration_cert'])
            else:
                sts.append('')

    shtrul_array.append(car_number)
    shtrul_array.append(region)
    shtrul_array.append(sts)

    return shtrul_array

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

    time.sleep(4)

    if check_exists_by_xpath("//button[@class='close_modal_window']"):
        button = driver.find_element_by_xpath("//button[@class='close_modal_window']")
        button.click()
        time.sleep(3)

    fines_count = len(driver.find_elements_by_xpath("//div[@class='checkResult']/ul[@class='finesItem']"))

    for i in range(fines_count - 1):
        current_fine = Fine
        date_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-datedecis']")[
            i].text
        decree_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                   "ul[@class='finesItem']/li/span[@class='field fine-datepost']")[
            i].text
        cost_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-summa']")[i].text

        current_fine.date = parser.parse(date_str.split()[0])
        current_fine.time = parser.parse(date_str.split()[2])
        current_fine.decree = decree_str.split()[0]
        current_fine.cost = cost_str.split()[0]

        fines_array.append(current_fine)

    driver.close()

    return fines_array

shtruls = get_shtruls_from_api()
for i in range(len(shtruls[0])):
    parse_info(shtruls[0][i], shtruls[1][i], shtruls[2][i])

#parse_info('У468ВХ', '797', '9931918970')
