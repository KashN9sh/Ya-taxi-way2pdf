import time
import json
import requests
import Taximeter_api
import Config
import Database
import datetime
import Database_2
import telebot

db = Database_2.DataBase()

test_token = "519348832:AAFBNvbmusq0i89fsMdL9o1pVI_mEHFt5Sc"
bot = telebot.TeleBot(test_token)


def bla():
    url = "https://yataxist.amocrm.ru/private/api/auth.php?type=json"
    dic = {"USER_LOGIN": "pankratiev.petr@yandex.ru",
           "USER_HASH": "720bca41100ad774361b9b5d2af9ed40"}

    requests.Session()
    with requests.Session() as s:
        resp = s.post(url, dic)
        print(resp.json())

        url2 = "https://yataxist.amocrm.ru/api/v2/catalogs"
        resp = s.get(url2)
        print(resp.json())

        #url2 = "https://yataxist.amocrm.ru/api/v2/catalog_elements"
        #resp = s.get(url2, params={"catalog_id": 18007567})
        #print(resp.json())

def bla2():
    url = "https://passport.yandex.ru/auth?retpath=https%3A%2F%2Flk.taximeter.yandex.ru%2F"
    url2 = "https://lk.taximeter.yandex.ru/order/10fb76836e254bba84189a8106e8a168"
    # requests.Session()
    postdata = {'yandex_login': 'skind-oleg', 'Password': 'loop1824'}
    with requests.Session() as s:
        s.auth = ("skind-oleg", "loop1824")
        resp = s.post(url, data=postdata)
        print(resp.text)

# bla2()
# te_id = "04bf34af46124c3f8e357f50e2d99b96"
# resp = Taximeter_api.get_status(Config.token_taximeter, te_id)
# print(resp)
# resp = Taximeter_api.get_list_drivers(Config.token_taximeter)
# print(json.dumps(resp, ensure_ascii=False, indent=4))
#
# db = Database.DataBase()
# print(db.get_statement(datetime.date.today(), 10500))


import signal


flag = True


def sigint_handler(signum, frame):
    global flag
    flag = False
    print('sent', signum)

signal.signal(signal.SIGTERM, sigint_handler)


if __name__ == "__main__":
    # global flag
    while flag:
        print(">")
        time.sleep(5)

