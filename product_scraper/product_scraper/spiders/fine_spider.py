import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from uuid import uuid4
import datetime
import pandas as pd
import itertools

dateFormatter = "%d.%m.%Y %H:%M"
hours = 1
hours_added = datetime.timedelta(hours = hours)

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
    car_number: str
    region: str
    sts: str
    driver_id: str
    car_id: str

    def __init__(self, car_number, region, sts, driver_id, car_id):
        self.car_number = car_number
        self.region = region
        self.sts = sts
        self.driver_id = driver_id
        self.car_id = car_id

def get_shtruls_from_api():
    url_auth = 'https://fleet-api.taxi.yandex.net/v1/parks/driver-profiles/list'

    headers = {
        'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
        'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
    }

    shtrul_array = []

    data = {"query": {"park": {"id": "e96b6ddf4309416ba66bc8f801bc847f",
                               "driver_profile": {"work_rule_id": ["de98224d038a4f98a10b0fd8bf967efe", ],
                                                  # "badd1c9d6b6b4e9fb9e0b48367850467"],
                                                  "work_status": ["working", "not_working"]}}}}
    response = requests.post(url_auth, headers=headers, json=data)

    for i in range(len(response.json()['driver_profiles'])):
        if 'car' in response.json()['driver_profiles'][i]:
            car_number = response.json()['driver_profiles'][i]['car']['number'][0:6]
            car_id = response.json()['driver_profiles'][i]['car']['id']
            region = response.json()['driver_profiles'][i]['car']['number'][6:]
            if 'registration_cert' in response.json()['driver_profiles'][i]['car']:
                sts = response.json()['driver_profiles'][i]['car']['registration_cert']
            else:
                sts = ''
            driver_id = response.json()['driver_profiles'][i]['driver_profile']['id']

        shtrul_array.append(Shtrul(car_number, region, sts, driver_id, car_id))

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
    time.sleep(1)
    button.click()

    time.sleep(25)

    if check_exists_by_xpath("//button[@class='close_modal_window']"):
        button = driver.find_element_by_xpath("//button[@class='close_modal_window']")
        button.click()
        time.sleep(3)

    fines_count = len(driver.find_elements_by_xpath("//div[@class='checkResult']/ul[@class='finesItem']"))

    for i in range(fines_count):
        date_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-datedecis']")[i].text

        decree_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                   "ul[@class='finesItem']/li/span[@class='field fine-datepost']")[i].text
        cost_str = driver.find_elements_by_xpath("//div[@class='checkResult']/"
                                                 "ul[@class='finesItem']/li/span[@class='field fine-summa']")[i].text

        fines_array.append(Fine(date_str.split()[0], date_str.split()[2], decree_str.split()[0], cost_str.split()[0]))

    driver.close()

    return fines_array

def check_orders(fines_array, shtrul):
    final_fines_array = []
    fines = []
    shtruls = []
    URL_AUTH = 'https://fleet-api.taxi.yandex.net/v1/parks/orders/list'

    headers = {
        'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
        'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
    }

    if len(fines_array) != 0:
        for i in range(len(fines_array)):
            data = {
                "limit": 100,
                "query": {
                    "park": {
                        "id": "e96b6ddf4309416ba66bc8f801bc847f",
                        "car": {"id": shtrul.car_id},
                        #"driver_profile": {"id": shtrul.driver_id},
                        "order": {
                            "booked_at": {
                                "from": (datetime.datetime.strptime(fines_array[i].date + ' ' + fines_array[i].time,
                                                          dateFormatter).astimezone().replace(microsecond=0) - hours_added).isoformat(),

                                 "to": (datetime.datetime.strptime(fines_array[i].date + ' ' + fines_array[i].time,
                                                          dateFormatter).astimezone().replace(microsecond=0) + hours_added).isoformat()
                            }
                        }
                    }
                }
            }

            response = requests.post(URL_AUTH, headers=headers, json=data)

            if len(response.json()['orders']) != 0:
                fines.append(fines_array[i])
                shtruls.append(response.json()['orders'][0]['driver_profile'])
                #print(fines_array[i].decree)
            #print(response.status_code)
            #print(response.json())
            time.sleep(0.5)
    final_fines_array.append(fines)
    final_fines_array.append(shtruls)
    return final_fines_array

def print_fines_array(fines_array, bd, carriers, car_number):
    f = open("decrees.txt", "a")
    flag = True
    decrees =[]
    URL_AUTH = 'https://fleet-api.taxi.yandex.net/v2/parks/driver-profiles/transactions'

    for _ in range(len(carriers)):
        decrees.append([])

    for i in range(len(fines_array[0])):
        for decree in bd:
            if decree == fines_array[0][i].decree + '\n':
                flag = False
                break

        if flag:
            bd.append(fines_array[0][i].decree + '\n')
            print(i + 1)
            headers = {
                # 'Accept-Language':'ru',
                'X-Client-ID': 'taxi/park/e96b6ddf4309416ba66bc8f801bc847f',
                'X-API-Key': 'zohhKIuBMdIpJTEiKzrePMQIUuHXDyNFgRrSf',
                'X-Idempotency-Token': str(uuid4())
            }

            data = {"amount": '-' + fines_array[0][i].cost,
                    "category_id": 'partner_service_manual',
                    "description": f'списание средств для оплаты штрафа постановление № "{fines_array[0][i].decree}" от {fines_array[0][i].date}',
                    "driver_profile_id": fines_array[1][i]['id'],
                    "park_id": "e96b6ddf4309416ba66bc8f801bc847f"}

            response = requests.post(URL_AUTH, headers=headers, json=data)
            print(response.status_code)
            print(response.json())

            data = {"amount": fines_array[0][i].cost,
                    "category_id": 'partner_service_manual',
                    "description": f'деньги для оплаты штрафа постановление № "{fines_array[0][i].decree}" от {fines_array[0][i].date}',
                    "driver_profile_id": '023e46118ba74f1c92f2a7189af6c68b',
                    "park_id": "e96b6ddf4309416ba66bc8f801bc847f"}

            response = requests.post(URL_AUTH, headers=headers, json=data)
            print(response.status_code)
            print(response.json())

            f.write('\n')
            f.write(fines_array[0][i].decree)

            for j in range(len(carriers)):
                if carriers[j] == fines_array[1][i]['name']:
                    break
            decrees[j].append(fines_array[0][i].decree + ' ' + fines_array[0][i].cost + ' ' + fines_array[0][i].date)

    if len(fines_array[0]) != 0:
        decrees = list(map(list, itertools.zip_longest(*decrees, fillvalue=None)))

        data_for_excel = pd.DataFrame(data = decrees, columns = carriers)

        writer = pd.ExcelWriter(f'{car_number}.xlsx')

        data_for_excel.to_excel(writer, index=False,
                                sheet_name=datetime.datetime.now().date().strftime("%d.%m.%Y"))

        # Auto-adjust columns' width
        for column in data_for_excel:
            column_width = max(data_for_excel[column].astype(str).map(len).max(), len(column))
            col_idx = data_for_excel.columns.get_loc(column)
            writer.sheets[datetime.datetime.now().date().strftime("%d.%m.%Y")].set_column(col_idx, col_idx, column_width)

        writer.save()


def get_decrees_from_bd():
    f = open("decrees.txt", "r")
    decrees = []
    for line in f:
        decrees.append(line)
    f.close()
    return decrees

# def fines_pay(shtrul, fines_array):

decrees_in_bd = get_decrees_from_bd()
shtruls = get_shtruls_from_api()
first_fines_array = []
final_fines_array = []

#все машины
'''
for i in range(len(shtruls)):
    first_fines_array.append(parse_info(shtruls[i].car_number, shtruls[i].region, shtruls[i].sts))
    final_fines_array.append(check_orders(first_fines_array[i], shtruls[i]))

    names =[]
    for carrier in final_fines_array[i][1]:
        flag = True

        if len(names) == 0:
            names.append(carrier['name'])

        for name in names:
            if name == carrier['name']:
                flag = False

        if flag: names.append(carrier['name'])

    print_fines_array(final_fines_array[i], decrees_in_bd, names, shtruls[i].car_number)
'''

#одна машина
'''
for i in range(len(shtruls)):
    if shtruls[i].car_number == 'М586АМ':
        first_fines_array.append(parse_info(shtruls[i].car_number, shtruls[i].region, shtruls[i].sts))
        final_fines_array.append(check_orders(first_fines_array[0], shtruls[i]))

        names =[]
        for carrier in final_fines_array[0][1]:
            flag = True

            if len(names) == 0:
                names.append(carrier['name'])

            for name in names:
                if name == carrier['name']:
                    flag = False

            if flag: names.append(carrier['name'])

        print_fines_array(final_fines_array[0], decrees_in_bd, names, shtruls[i].car_number)'''

# parse_info('У468ВХ', '797', '9931918970')
