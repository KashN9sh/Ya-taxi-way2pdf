import logging
import requests
from datetime import timedelta


def _check_result(response):
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        raise LookupError
    elif response.status_code == 400:
        raise ValueError


def get_list_drivers(token):
    url = "https://taximeter.yandex.rostaxi.org/api/driver/list"
    resp = requests.get(url, params={"apikey": token})
    return _check_result(resp)


def get_driver(token, id):
    url = "https://taximeter.yandex.rostaxi.org/api/driver/get"
    resp = requests.get(url, params={"apikey": token, "id": id})
    return _check_result(resp)


def get_list_balances(token):
    url = "https://taximeter.yandex.rostaxi.org/api/driver/balance"
    resp = requests.get(url, params={"apikey": token})
    return _check_result(resp)


def get_balance(token, id):
    url = "https://taximeter.yandex.rostaxi.org/api/driver/balance"
    resp = requests.get(url, params={"apikey": token})
    return _check_result(resp)[id]


def reduce_balance(token, id, sum):
    url = "https://taximeter.yandex.rostaxi.org/api/driver/balance/minus"
    resp = requests.get(url, params={"apikey": token,
                                     "driver": id,
                                     "sum": sum,
                                     "group": "Вывод средств водителю",
                                     "description": "Test"})
    return resp.status_code


def status_to_str(status):
    stat = {0: "Поиск машины",
            10: "Выехал",
            20: "Ожидает",
            30: "Отзвонились",
            40: "В пути",
            50: "Завершен",
            60: "Отменен по вине водителя",
            70: "Отменен клиентом",
            80: "expired"}
    return stat.get(status, "unknown")


def get_status(token, order_id):
    url = "https://taximeter.yandex.rostaxi.org/api/request/status"
    resp = requests.get(url, params={"apikey": token,
                                     "id": order_id})
    return _check_result(resp)


def new_oreder(token, name, phone, travel, dt, comment=""):
    tariff_id = "a9979490934443769319a85499c6d09c"
    type_id = "28e60db9c795429987213f75155b5c6c"
    url = "https://taximeter.yandex.rostaxi.org/api/request/setcar"
    td = timedelta(minutes=10)
    dt += td
    resp = requests.get(url, params={"apikey": token,
                                     "name": name,
                                     "phone1": phone,
                                     "date": dt.date(),
                                     "time": dt.strftime("%H:%M"),
                                     "show-phone": True,
                                     "rule": type_id,
                                     "tariff": tariff_id,
                                     "description": comment,
                                     "AddressFromCity": travel.adr_from.city,
                                     "AddressFromStreet": travel.adr_from.street,
                                     "AddressFromHouse": travel.adr_from.house,
                                     "AddressToCity": travel.adr_where.city,
                                     "AddressToStreet": travel.adr_where.street,
                                     "AddressToHouse": travel.adr_where.house})
    return _check_result(resp)


def cancel_order(token, ya_id, comment):
    url = "https://taximeter.yandex.rostaxi.org/api/request/cancel"
    resp = requests.get(url, params={"apikey": token,
                                     "id": ya_id,
                                     "comment": comment})
    return _check_result(resp)


def get_car(token, vehicle_id):
    url = "https://taximeter.yandex.rostaxi.org/api/car/get"
    resp = requests.get(url, params={"apikey": token,
                                     "id": vehicle_id})
    return _check_result(resp)


def get_gps(token, driver_id):
    url = "https://taximeter.yandex.rostaxi.org/api/gps/get"
    resp = requests.get(url, params={"apikey": token,
                                     "id": driver_id})
    return _check_result(resp)


if __name__ == "__main__":
    pass
