import logging
import csv
import json

import Database
import Taximeter_api
import Config
from Config import logger

logger.setLevel(logging.DEBUG)


def get_list(path):
    data = list()
    with open(path) as f:
        reader = csv.reader(f, delimiter=";")
        for norm_row in reader:
            # row = row.rstrip()
            dt = list()
            # norm_row = row.split(";")
            for dat in norm_row[0].split(" ", maxsplit=2):
                dt.append(dat.title())
            dt.append("-".join(reversed(norm_row[1].split("."))))
            for i in (2, 4, 3):
                dt.append(norm_row[i])
            try:
                if norm_row[8] == "":
                    dt.append("Заказана")
                else:
                    dt.append(norm_row[8])
            except IndexError:
                dt.append(None)
            try:
                dt.append(norm_row[10])
            except IndexError:
                dt.append(None)
            data.append(dt)
    return data


def import_zp_ab():
    db = Database.DataBase(Config.cfg_file)
    list_ab = get_list(Config.alfabank_file)
    logger.info("len ab: {}".format(len(list_ab)))
    db.update_zp_alfa(list_ab)
    for i in list_ab:
        logger.info(i)


def import_taximeter(token):
    db = Database.DataBase(Config.cfg_file)
    dict_ya = Taximeter_api.get_list_drivers(token)["drivers"]
    list_ya = list()
    for id_driv in dict_ya.keys():
        lst = list()
        lst.append(id_driv)
        lst.append(dict_ya[id_driv]["FirstName"])
        lst.append(dict_ya[id_driv]["LastName"])
        lst.append(dict_ya[id_driv].get("Surname", ""))
        lst.append(dict_ya[id_driv].get("LicenseSeries", "")+dict_ya[id_driv].get("LicenseNumber", ""))
        tmp = dict_ya[id_driv].get("LicenseDateOf")
        if tmp is not None:
            tmp = tmp.split("T")[0]
        lst.append(tmp)
        tmp = dict_ya[id_driv].get("LicenseDateEnd")
        if tmp is not None:
            tmp = tmp.split("T")[0]
        lst.append(tmp)
        lst.append(dict_ya[id_driv]["Phones"].split("; "))

        list_ya.append(lst)
    db.update_yataxis(list_ya)
    logger.info("len ya: {}".format(len(list_ya)))
    for i in list_ya:
        logger.info(i)


def autho_zp_ab(login, password):
    pass


def autho_lk_zp(login, password):
    pass


if __name__ == "__main__":
    logger.info("start import")
    import_taximeter(Config.token_taximeter)
    #import_zp_ab()
    logger.info("end import")
