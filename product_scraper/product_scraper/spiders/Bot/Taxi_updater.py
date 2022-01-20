import time
import requests
import telebot
import Database_2
import Taximeter_api

from Config import token_taximeter
from Config import token_clients_bot
from Config import token_google

db = Database_2.DataBase()
bot = telebot.TeleBot(token_clients_bot)

test = [[293367935, "321b21809f934a85a788f37a77e5d212", 0, None], ]

def get_adr(ya_id):
    return ("Зеленоград", "", "к1624")

def get_test():
    return test


def get_time(latitude, longitude, address):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    loc = str(latitude) + "," + str(longitude)
    resp = requests.get(url, params={"key": token_google,
                                     "origin": loc,
                                     "destination": address,
                                     "departure_time": "now"})
    print(resp.url)
    return resp.json()["routes"][0]["legs"][0]["duration_in_traffic"]["value"]


def delete_message(id_telegram, id_message):
    if id_message and id_telegram:
        try:
            bot.delete_message(id_telegram, id_message - 1)
        except telebot.apihelper.ApiException:
            pass
        try:
            bot.delete_message(id_telegram, id_message)
        except telebot.apihelper.ApiException:
            pass

def updater():
    currents = db.get_currents()
    # currents = get_test()
    if len(currents) == 0:
        time.sleep(30)
        return
    for it in currents:
        id_telegram = it[0]
        ya_id = it[1]
        status = it[2]
        id_gps = it[3]
        try:
            resp = Taximeter_api.get_status(token_taximeter, ya_id)
            update = False
            try:
                if not resp["driver_id"] == "":
                    gps = Taximeter_api.get_gps(token_taximeter, resp["driver_id"])
                    if id_gps is None:
                        bebe = Taximeter_api.get_driver(token_taximeter, resp["driver_id"])
                        car = bebe["car"]
                        name = bebe["driver"]["LastName"] + " " + bebe["driver"]["FirstName"]
                        phone = bebe["driver"]["Phones"]
                        text = car["Mark"] + " " + car["ModelName"] + ", " + car["Color"] + ", " + car["Number"]\
                               + "\n" + name + "\n" + phone
                        bot.send_message(id_telegram, text)
                        adr = db.get_adr_from(ya_id)
                        # adr = get_adr(ya_id)
                        address = adr[0] + "+" + adr[1] + "+" + adr[2]
                        time_wait = get_time(gps["L"], gps["O"], address) + 120
                        # print("as")
                        msg = bot.send_location(id_telegram, gps["L"], gps["O"], live_period=time_wait)
                        id_gps = msg.message_id
                        # it[3] = id_gps
                        # print(id_gps)

                        update = True
                    else:
                        try:
                            bot.edit_message_live_location(gps["L"], gps["O"], chat_id=id_telegram, message_id=id_gps)
                        except telebot.apihelper.ApiException:
                            print("ups")
            except LookupError as err:
                # logger.exception("[WTF?]")
                print(err)
                continue
            if resp["status"] != status:
                status = resp["status"]
                # it[2] = status
                bot.send_message(id_telegram, Taximeter_api.status_to_str(status))
                update = True
                if status == 50:
                    db.delete_current(id_telegram)
                    delete_message(id_telegram, id_gps)
                    update = False
                if status >= 60:
                    db.delete_order(ya_id)
                    delete_message(id_telegram, id_gps)
                    update = False
            if update:
                db.upd_current(id_telegram, status, id_gps)
        except LookupError as err:
            # logger.exception("[WTF?]")
            print(err)
            db.delete_order(ya_id)


if __name__ == "__main__":
    while True:
        updater()
        time.sleep(2)
