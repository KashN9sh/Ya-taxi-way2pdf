from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error

import Config

from Config import logger


class DataBase:
    def __init__(self, cfg_file=Config.cfg_file):
        self._dbconfig = dict()
        self._read_db_config(cfg_file)

    def _read_db_config(self, filename, section="mysql_taxi"):
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                self._dbconfig[item[0]] = item[1]
        else:
            raise Exception("{0} not found in the {1} file".format(section, filename))

    def get_current_id(self, id_telegram):
        sql_sel = """
            SELECT
                `ya_id`
            FROM 
                `currents`
            WHERE
                `id_telegram` =  %(id_telegram)s;
        """
        ya_id = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_sel, {"id_telegram": id_telegram})
            ya_id = cur.fetchone()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")
        return ya_id

    def delete_current(self, id_telegram):
        sql_del = """
            DELETE FROM
                `currents`
            WHERE 
                `id_telegram` = %(id_telegram)s;
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_del, {"id_telegram": id_telegram})
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")

    def delete_order(self, ya_id):
        sql_del = """
            DELETE FROM
                `orders`
            WHERE 
                `ya_id` = %(ya_id)s;
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_del, {"ya_id": ya_id})
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")

    def add_current(self, id_telegram, orader, ya_num, ya_id, amount=None):
        sql_sel = """
            SELECT `id_address` FROM `addresses`
                WHERE `city` = %(city)s
                AND `street` = %(street)s
                AND `house` = %(house)s;
        """
        sql_ins_adr = """
            INSERT INTO `addresses` (`id_address`, `city`, `street`, `house`)
            VALUES (NULL, %(city)s, %(street)s, %(house)s);
        """
        sql_ins_ord = """
            INSERT INTO `orders` (`id_order`, `id_telegram`, `adr_from`, `adr_where`,
             `ya_num`, `ya_id`, `datetime`, `amount`)
            VALUES (NULL, %(id_telegram)s, %(adr_from)s, %(adr_where)s,
             %(ya_num)s, %(ya_id)s, NOW(), %(amount)s);
        """
        sql_ins_cur = """
            INSERT INTO 
               `currents` (`id_telegram`, `ya_id`, `status`, `id_gps`)
            VALUES 
                (%(id_telegram)s, %(ya_id)s,  0, NULL);
        """

        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_sel, orader.adr_from.to_dic())
            adr_from = cur.fetchone()
            if not adr_from:
                cur.execute(sql_ins_adr, orader.adr_from.to_dic())
                adr_from = cur.lastrowid
            cur.execute(sql_sel, orader.adr_where.to_dic())
            adr_where = cur.fetchone()
            if not adr_where:
                cur.execute(sql_ins_adr, orader.adr_where.to_dic())
                adr_where = cur.lastrowid
            cur.execute(sql_ins_ord, {"id_telegram": id_telegram,
                                      "adr_from": adr_from,
                                      "adr_where": adr_where,
                                      "ya_num": ya_num,
                                      "ya_id": ya_id,
                                      "amount": amount})
            cur.execute(sql_ins_cur, {"id_telegram": id_telegram,
                                      "ya_id": ya_id})
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")

    def upd_current(self, id_telegram, status, id_gps=None):
        sql_upd = """
            UPDATE `currents`
            SET
                `status` = %(status)s,
                `id_gps` = %(id_gps)s
            WHERE 
                `id_telegram` = %(id_telegram)s;
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_upd, {"id_telegram": id_telegram,
                                  "status": status,
                                  "id_gps": id_gps})
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")

    def get_currents(self):
        sql_sel = """
            SELECT `id_telegram`, `ya_id`, `status`, `id_gps`
            FROM `currents`;
        """
        response = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_sel)
            response = cur.fetchall()
            if response is None:
                response = []
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")
        return response

    def get_number(self, id_telegram):
        sql_sel = """
            SELECT `phone`
            FROM `clients`
            WHERE `id_telegram` = %(id_telegram)s;
        """
        phone = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_sel, {"id_telegram": id_telegram})
            resp = cur.fetchone()
            phone = resp[0]
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")
        return phone

    def add_client(self, id_telegram, phone):
        sql_sel = """
            SELECT venues.title, addresses.city, addresses.street, addresses.house, venues.id_venue 
            FROM `venues`, `addresses` 
            WHERE venues.id_telegram = %(id_telegram)s
            AND addresses.id_address = venues.id_address;
        """
        sql_ins = """
            INSERT IGNORE INTO `clients` (`id_telegram`, `phone`)
            VALUES (%(id_telegram)s, %(phone)s);
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_ins, {"id_telegram": id_telegram, "phone": phone})
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")

    def get_adr_from(self, ya_id):
        sql_sel = """
        SELECT 
            `city`, `street`, `house` 
        FROM
            `addresses` 
        WHERE 
            `id_address` IN (
                SELECT `adr_from` 
                FROM `orders` 
                WHERE `ya_id` = %(ya_id)s
                );
        """
        adr = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql_sel, {"ya_id": ya_id})
            resp = cur.fetchone()
            if resp:
                adr = resp[0]
            conn.commit()
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")
        return adr

    def test(self):
        sql = """SELECT * FROM orders"""
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
            cur.execute(sql)
            print(cur.fetchall())
            cur.close()
            conn.close()
        except Error:
            logger.exception("[WTF?]")
