import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from uuid import uuid4


class Fine:
    date: str
    time: str
    decree: str
    cost: str

    def __init__(self, date, time, decree, cost):
        self.date = date
        self.time = time
        self.decree = decree
        self.cost = cost

class Shtrul:
    car_number : str
    region : str
    sts : str
    driver_id : str

    def __init__(self, car_number, region, sts, driver_id):
        self.car_number = car_number
        self.region = region
        self.sts = sts
        self.driver_id = driver_id

def get_shtruls_from_api():
    url_auth = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'

    headers = {
        'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
        'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
    }

    shtrul_array = []

    data = {"query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f",
                               "driver_profile": {"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe",],
                                                                   #"badd1c9d6b6b4e9fb9e0b48367850467"],
                                                  "work_status": ["working", "not_working"]}}}}
    response = requests.post(url_auth, headers=headers, json=data)

    for i in range(len(response.json()['driver_profiles'])):
        if 'car' in response.json()['driver_profiles'][i]:
            car_number = response.json()['driver_profiles'][i]['car']['number'][0:6]
            region = response.json()['driver_profiles'][i]['car']['number'][6:]
            if 'registration_cert' in response.json()['driver_profiles'][i]['car']:
                sts = response.json()['driver_profiles'][i]['car']['registration_cert']
            else:
                sts = ''
            driver_id = response.json()['driver_profiles'][i]['driver_profile']['id']

        shtrul_array.append(Shtrul(car_number, region, sts, driver_id))

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

    for i in range(fines_count):

        date_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-datedecis']")[
            i].text

        decree_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                   "ul[@class='finesItem']/li/span[@class='field fine-datepost']")[
            i].text
        cost_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-summa']")[i].text

        fines_array.append(Fine(date_str.split()[0], date_str.split()[2], decree_str.split()[0], cost_str.split()[0]))

    driver.close()

    return fines_array

def print_fines_array(array, shtrul):
    print(len(array))
    for i in range(len(array)):
        for j in range(len(array[i])):
            print(j + 1)
            data = {"amount": '-' + array[i][j].cost,
                    "category_id": 'partner_service_manual',
                    "description": f'списание средств для оплаты штрафа постановление № "{array[i][j].decree}"',
                    "driver_profile_id": shtrul.driver_id,
                    "park_id": "e96b6ddf4309416ba66bc8f801bc847f"}
            print(data['description'])
            print('---------------------')
        print('#################')

#def fines_pay(shtrul, fines_array):



shtruls = get_shtruls_from_api()
fines_array = []
for i in range(len(shtruls)):
    fines_array.append(parse_info(shtruls[i].car_number, shtruls[i].region, shtruls[i].sts))
    print_fines_array(fines_array,shtruls[i])
#parse_info('У468ВХ', '797', '9931918970')


