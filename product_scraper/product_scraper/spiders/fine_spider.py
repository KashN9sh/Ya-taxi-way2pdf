import random
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import requests
from uuid import uuid4
import datetime
import pandas as pd
import itertools
from PyQt5 import QtWidgets,QtCore, QtGui
import fines
import sys
import xlsxwriter
import os

dateFormatter = "%d.%m.%Y %H:%M"
hours = 8
hours_added = datetime.timedelta(hours = hours)

class Fine:
    date: str
    time: str
    decree: str
    cost: str
    color: str

    def __init__(self, date, time, decree, cost, color):
        self.date = date
        self.time = time
        self.decree = decree
        self.cost = cost
        self.color = color

class Shtrul:
    car_number: str
    region: str
    sts: list
    driver_id: str
    car_id: list

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
                                                  #"work_status": ["working", "not_working"]
                                                  }}}}
    response1 = requests.post(url_auth, headers=headers, json=data)

    for i in range(len(response1.json()['driver_profiles'])):
        car_id = []
        sts = []
        if 'car' in response1.json()['driver_profiles'][i]:
            car_number = response1.json()['driver_profiles'][i]['car']['number'][0:6]
            car_id.append(response1.json()['driver_profiles'][i]['car']['id'])
            region = response1.json()['driver_profiles'][i]['car']['number'][6:]
            if 'registration_cert' in response1.json()['driver_profiles'][i]['car']:
                sts.append(str(response1.json()['driver_profiles'][i]['car']['registration_cert']))
            else:
                sts = []
            driver_id = response1.json()['driver_profiles'][i]['driver_profile']['id']

        URL_AUTH = 'https://fleet-api.taxi.yandex.net/v1/parks/cars/list'

        flag2 = True

        flag1 = True
        flag3 = True

        for shtrul in shtrul_array:
            if shtrul.car_number == car_number and region == shtrul.region:
                flag2 = False

                flag3 = False
                for Sts in shtrul.sts:
                    if not flag3 and Sts == sts[0]:
                        flag3 = True

                flag1 = False
                for Id in shtrul.car_id:
                    if not flag1 and Id == car_id[0]:
                        flag1 = True

                if not flag1:
                    shtrul.car_id.append(response1.json()['driver_profiles'][i]['car']['id'])

                if not flag3:
                    shtrul.sts.append(response1.json()['driver_profiles'][i]['car']['registration_cert'])



        if flag2:
            if len(shtrul_array) == 0 or (flag1 and flag3) and car_number != "COURIE":
                shtrul_array.append(Shtrul(car_number, region, sts, driver_id, car_id))

        #if flag:
            '''
            data = {"offset": 0,
                    "limit": 1000,
                    "query": {
                        "park": {
                            "id": "e96b6ddf4309416ba66bc8f801bc847f",
                        }
                    }
                    }
            
            response = requests.post(URL_AUTH, headers=headers, json=data)
            total = int(response.json()['total'])

            for k in range(total // 1000):
                response = requests.post(URL_AUTH, headers=headers, json=data)
                for j in range(len(response.json()['cars'])):
                    if response.json()['cars'][j]['number'] == car_number + region and response.json()['cars'][j]['id'] != car_id[0]:
                        car_id.append(response.json()['cars'][j]['id'])

                data['offset'] += 1000'''

            #shtrul_array.append(Shtrul(car_number, region, sts, driver_id, car_id))
        print(car_number)

    return shtrul_array

def parse_info(gos_reg, region, registration):
    fines_array = []

    for i in range(len(registration)):
        fines_url = f'https://гибдд.рф/check/fines#{gos_reg}+{region}+{registration[i]}'

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

            color_str = "Black"

            prosrochka = len(driver.find_elements_by_xpath("//span[@class='sentfssp']"))
            sale = len(driver.find_elements_by_xpath("//span[@class='sum50prc']"))

            if i < prosrochka:
                color_str = "Red"
            elif sale > fines_count - i:
                color_str = "Green"

            fines_array.append(Fine(date_str.split()[0], date_str.split()[2], decree_str.split()[0], cost_str.split()[0], color_str))

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
            for j in range(len(shtrul.car_id)):
                data = {
                    "limit": 100,
                    "query": {
                        "park": {
                            "id": "e96b6ddf4309416ba66bc8f801bc847f",
                            "car": {"id": shtrul.car_id[j]}, #beba76aa0b7e49733bf6c92c2d89ff58
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

                if response.status_code == 200:
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

'''def print_fines_array(fines_array, bd, carriers, car_number):
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

        writer.save()'''


def get_decrees_from_bd():
    f = open("decrees.txt", "r")
    decrees = []
    for line in f:
        decrees.append(line)
    f.close()
    return decrees

# def fines_pay(shtrul, fines_array):

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


class App(QtWidgets.QMainWindow, fines.Ui_MainWindow):
    decrees_in_bd = []
    shtruls = []
    first_fines_array = []
    final_fines_array = []
    car_number = ''

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.BtnGetFines.clicked.connect(self.Work1)
        self.BtgEbatShtrule1.clicked.connect(self.Work2)
        self.decrees_in_bd = get_decrees_from_bd()
        self.shtruls = get_shtruls_from_api()

        for shtrul in self.shtruls:
            self.listWidget.addItem(shtrul.car_number)

    def print_fines_array(self, fines_array, bd, carriers, car_number):
        f = open("decrees.txt", "a")
        decrees = []
        URL_AUTH = 'https://fleet-api.taxi.yandex.net/v2/parks/driver-profiles/transactions'

        for _ in range(len(carriers)):
            decrees.append([])

        for i in range(len(fines_array[0])):
            flag = True

            if not self.listWidget_2.item(i).checkState():
                flag = False

            for decree in bd:
                if (decree == fines_array[0][i].decree + '\n' or decree == fines_array[0][i].decree) and (self.listWidget_2.item(i).checkState()):
                    flag = False
                    self.listWidget1.addItem(f'средства по постановлению "{fines_array[0][i].decree}" от {fines_array[0][i].date} уже списаны')

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
                self.listWidget1.addItem(f'списание средств для оплаты штрафа постановление № "{fines_array[0][i].decree}" от {fines_array[0][i].date} {fines_array[1][i]["name"]} ')

                data = {"amount": fines_array[0][i].cost,
                        "category_id": 'partner_service_manual',
                        "description": f'деньги для оплаты штрафа постановление № "{fines_array[0][i].decree}" от {fines_array[0][i].date} {fines_array[1][i]["name"]} ',
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
                decrees[j].append(
                    fines_array[0][i].decree + ' ' + fines_array[0][i].cost + ' ' + fines_array[0][i].date)

        if len(fines_array[0]) != 0:
            decrees = list(map(list, itertools.zip_longest(*decrees, fillvalue=None)))

            data_for_excel = pd.DataFrame(data=decrees, columns=carriers)

            if not os.path.exists(str(car_number)):
                os.mkdir(str(car_number))

            name = str(car_number) + '/' + datetime.datetime.now().strftime("%d%m%Y%H%M%S") + '.xlsx'

            workbook = xlsxwriter.Workbook(name)
            worksheet = workbook.add_worksheet(datetime.datetime.now().date().strftime("%d.%m.%Y "))

            writer = pd.ExcelWriter(name)

            data_for_excel.to_excel(writer, index=False,
                                    sheet_name=datetime.datetime.now().date().strftime("%d.%m.%Y "))

            # Auto-adjust columns' width
            for column in data_for_excel:
                column_width = max(data_for_excel[column].astype(str).map(len).max(), len(column))
                col_idx = data_for_excel.columns.get_loc(column)
                writer.sheets[datetime.datetime.now().date().strftime("%d.%m.%Y ")].set_column(col_idx, col_idx,
                                                                                              column_width)

            writer.save()

    def Work1(self):
        self.first_fines_array.clear()
        self.final_fines_array.clear()

        for i in range(self.listWidget_2.count()):
            self.listWidget_2.takeItem(self.listWidget_2.row(self.listWidget_2.item(0)))

        self.car_number = self.shtruls[self.listWidget.currentRow()].car_number

        self.first_fines_array.append(parse_info(self.shtruls[self.listWidget.currentRow()].car_number,
                                            self.shtruls[self.listWidget.currentRow()].region,
                                            self.shtruls[self.listWidget.currentRow()].sts))
        self.final_fines_array.append(check_orders(self.first_fines_array[0],
                                              self.shtruls[self.listWidget.currentRow()]))

        for i in range(len(self.final_fines_array[0][0])):
            item = QtWidgets.QListWidgetItem()
            item.setText(self.final_fines_array[0][1][i]['name'] + ' ' +
                                      self.final_fines_array[0][0][i].decree + ' ' +
                                      self.final_fines_array[0][0][i].date + ' ' + self.final_fines_array[0][0][i].time + ' ' +
                                      self.final_fines_array[0][0][i].cost)
            item.setForeground(QtGui.QColor(self.final_fines_array[0][0][i].color))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget_2.addItem(item)

    def Work2(self):
        names = []
        for carrier in self.final_fines_array[0][1]:
            flag = True

            if len(names) == 0:
                names.append(carrier['name'])

            for name in names:
                if name == carrier['name']:
                    flag = False

            if flag: names.append(carrier['name'])

        self.print_fines_array(self.final_fines_array[0], self.decrees_in_bd, names, self.car_number)





def main():
    app = QtWidgets.QApplication(sys.argv)
    window = App()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()

# parse_info('У468ВХ', '797', '9931918970')
