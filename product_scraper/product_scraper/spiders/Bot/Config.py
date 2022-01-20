import datetime
import os
import json
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("YaTaxist")

handler = RotatingFileHandler('bot.log', maxBytes=50000, backupCount=10)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("[%(asctime)s] %(filename)s:%(lineno)d %(levelname)-8s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

commission = 1.03
limit = 2000
delta = 500


dispatchs = [
    275413060,
    293367935,
    424533573,
    410270179
]

admins = [
    293367935
]

apikey = "2009063546:AAGeofaYR2nMw1zH6Z2xcCPbCHacSA5kwJo"
test_token = "519348832:AAFBNvbmusq0i89fsMdL9o1pVI_mEHFt5Sc"
'''token_drivers_bot = "414215310:AAH1BnEc8OMtBmuvOfsO0nqnfj0zUSuCkNM"
token_clients_bot = "538609337:AAFGggN0-6MEhfDon6WlS730mOLUW-Wv2e8"'''
token_drivers_bot = apikey
token_clients_bot = apikey
token_taximeter = "811e304d23804252a794e84dddbbeacc"
token_google = "AIzaSyCWBnM6Yg77n0r6hWMWCWqWGwcQhcN2jvM"

URL_BASE = "https://api.telegram.org/bot"

calend_file = os.path.join(os.path.dirname(__file__), "calend.json")

template_file_xls = os.path.join(os.path.dirname(__file__), "Temp1.xls")

cfg_file = os.path.join(os.path.dirname(__file__), "config.ini")

last_menu_file = os.path.join(os.path.dirname(__file__), "./data/last_menu.json")

alfabank_file = os.path.join(os.path.dirname(__file__),  "./data/alfabank.csv")

taximania = os.path.join(os.path.dirname(__file__),  "./data/taximania/{}")

statement_file = os.path.join(os.path.dirname(__file__), "./data/773573156381_ИП_ПАНКРАТЬЕВ_ПЕТР_{}.xls")

working_time_start = datetime.time(hour=10,
                                   minute=0)
working_time_end = datetime.time(hour=17,
                                 minute=0)


def jsonKeys2str(x):
    if isinstance(x, dict):
        return {int(k): v for k, v in x.items()}
    return x


calend = None
with open(calend_file, "rt", encoding="utf-8") as file:
    calend = json.load(file, object_hook=jsonKeys2str)
