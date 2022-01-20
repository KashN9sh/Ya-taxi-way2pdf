from configparser import ConfigParser
from mysql.connector import MySQLConnection, Error, IntegrityError

import Taximeter_api
import Config

from Config import logger


class DataBase:
    def __init__(self, cfg_file=Config.cfg_file):
        self._dbconfig = dict()
        self._read_db_config(cfg_file)

    def _read_db_config(self, filename, section="mysql"):
        parser = ConfigParser()
        parser.read(filename)

        if parser.has_section(section):
            items = parser.items(section)
            for item in items:
                self._dbconfig[item[0]] = item[1]
        else:
            raise Exception("{0} not found in the {1} file".format(section, filename))

    def update_zp_alfa(self, list):
        sql_sel_id_driver = """
            SELECT `id_driver` FROM `drivers` 
                WHERE `first_name` = %(first_name)s
                AND `last_name` = %(last_name)s
                AND SUBSTRING_INDEX(surname, ' ', 1) = %(surname)s;
        """
        sql_ins_zp_alfa= """
            INSERT INTO `zp_alfa` (`id_driver`, `id_alfa`, `account_number`, `status_card`, `active_to`)
            VALUES (%(id_driver)s, %(id_alfa)s, %(account_number)s, %(status_card)s, %(active_to)s);
        """
        sql_upd_zp_alfa = """
            UPDATE `zp_alfa` 
            SET 
                `id_alfa` = %(id_alfa)s,
                `account_number` = %(account_number)s,
                `status_card` = %(status_card)s,
                `active_to` = %(active_to)s
            WHERE
                `id_driver` = %(id_driver)s;
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
        except Error:
            logger.exception("[WTF?]")
        else:
            for row in list:
                # print(row)
                try:
                    cur = conn.cursor(buffered=True)
                    cur.execute(sql_sel_id_driver, {"first_name": row[1],
                                                    "last_name": row[0],
                                                    "surname": row[2].split(' ')[0]})
                                                    # "birth_date": row[3],
                                                    # "passport": row[4]})
                    resp = cur.fetchone()
                    if resp is None:
                        pass
                    else:
                        id_driver = resp[0]
                        try:
                            cur.execute(sql_ins_zp_alfa, {"id_driver": id_driver,
                                                          "id_alfa": row[5],
                                                          "account_number": row[6],
                                                          "status_card": row[7],
                                                          "active_to": row[8]})
                        except IntegrityError:
                            # print("update")
                            cur.execute(sql_upd_zp_alfa, {"id_driver": id_driver,
                                                          "id_alfa": row[5],
                                                          "account_number": row[6],
                                                          "status_card": row[7],
                                                          "active_to": row[8]})
                        except Error:
                            logger.exception("[WTF?]")
                        finally:
                            conn.commit()
                    cur.close()
                except Exception:
                    pass
        finally:
            conn.close()

    def update_yataxis(self, list):
        sql_sel_id_driver = """
            SELECT `id_driver` FROM `drivers` WHERE `id_yataxi` = %(id_yataxi)s;
        """
        sql_ins_drivers = """
            INSERT INTO `drivers` 
            (`id_driver`, `first_name`, `last_name`, `surname`, `id_yataxi`,
             `driver_license`, `license_date_of`, `license_date_end`)
            VALUES 
            (NULL, %(first_name)s, %(last_name)s, %(surname)s, %(id_yataxi)s,
             %(driver_license)s, %(license_date_of)s, %(license_date_end)s);
        """
        sql_ins_phones = """
            INSERT INTO `phones` (`id_driver`, `phone`)
            VALUES (LAST_INSERT_ID(), %(phone)s);
        """
        sql_upd_phones = """
            INSERT INTO `phones` (`id_driver`, `phone`)
            VALUES (%(id_driver)s, %(phone)s);
        """
        sql_upd_drivers = """
            UPDATE `drivers` 
            SET 
                `first_name` = %(first_name)s,
                `last_name` = %(last_name)s,
                `surname` = %(surname)s,
                `driver_license` = COALESCE(%(driver_license)s, `driver_license`),
                `license_date_of` = COALESCE(%(license_date_of)s, `license_date_of`),
                `license_date_end` = COALESCE(%(license_date_end)s, `license_date_end`)
            WHERE
                `id_driver` = %(id_driver)s;
        """
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            for row in list:
                cur.execute(sql_sel_id_driver, {"id_yataxi": row[0]})
                resp = cur.fetchone()
                if resp is not None:
                    id_driver = resp[0]
                    cur.execute(sql_upd_drivers, {"id_driver": id_driver,
                                                  "first_name": row[1],
                                                  "last_name": row[2],
                                                  "surname": row[3],
                                                  "id_yataxi": row[0],
                                                  "driver_license": row[4],
                                                  "license_date_of": row[5],
                                                  "license_date_end": row[6]})
                    for tmp in row[7]:
                        try:
                            cur.execute(sql_upd_phones, {"id_driver": id_driver,
                                                         "phone": tmp})
                        except IntegrityError:
                            pass
                        except Error:
                            logger.exception("[WTF?]")
                    conn.commit()
                else:
                    cur.execute(sql_ins_drivers, {"first_name": row[1],
                                                  "last_name": row[2],
                                                  "surname": row[3],
                                                  "id_yataxi": row[0],
                                                  "driver_license": row[4],
                                                  "license_date_of": row[5],
                                                  "license_date_end": row[6]})
                    for tmp in row[7]:
                        try:
                            cur.execute(sql_ins_phones, {"phone": tmp})
                        except Error:
                            logger.exception("[WTF?]")
                    conn.commit()
        finally:
            cur.close()
            conn.close()

    def add_telegram_driver(self, phone, id_telegram):
        sql_sel = """
            SELECT `first_name`, `surname`, `id_driver` FROM `drivers` WHERE `id_driver` IN
            (SELECT `id_driver` FROM `phones` WHERE `phone` = %(phone)s);
        """
        sql_ins = """
            INSERT INTO `telegrams` (`id_driver`, `id_telegram`)
            VALUES (%(id_driver)s, %(id_telegram)s);
        """
        sql_upd = """
            UPDATE `telegrams` 
            SET 
                `id_driver` = %(id_driver)s
            WHERE
                `id_telegram` = %(id_telegram)s;
        """
        name = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel, {"phone": phone})
            resp = cur.fetchone()

            try:
                if resp is not None:
                    name = " ".join([resp[0], resp[1]])
                    try:
                        cur.execute(sql_ins, {"id_driver": resp[2], "id_telegram": id_telegram})
                    except IntegrityError:
                        cur.execute(sql_upd, {"id_driver": resp[2], "id_telegram": id_telegram})
                else:
                        cur.execute(sql_ins, {"id_driver": None, "id_telegram": id_telegram})
            except IntegrityError:
                pass
            except Error:
                logger.exception("[WTF?]")
            else:
                conn.commit()
        finally:
            cur.close()
            conn.close()

        return name

    def available(self, id_telegram):
        sql_sel_status = """
            SELECT `status_card` FROM `zp_alfa` WHERE `id_driver` IN
            (SELECT `id_driver` FROM `telegrams` WHERE `id_telegram` = %(id_telegram)s);
        """
        response = "Не заказана"
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel_status, {"id_telegram": id_telegram})
            resp = cur.fetchone()
            if resp is not None:
                response = resp[0]

        return response

    def add_payments(self, id_telegram, amount, date):
        sql_sel_id_payment = """
            SELECT `amount` FROM `payments` WHERE 
            `id_driver` = %(id_driver)s
            AND `date_payment` = %(date_payment)s;
        """
        sql_sel_id_driver = """
             SELECT `id_driver` FROM `telegrams` WHERE `id_telegram` = %(id_telegram)s;
        """
        sql_ins_payments = """
            INSERT INTO `payments` (`id_payment`, `id_driver`, `amount`, `date_payment`)
            VALUES (NULL, %(id_driver)s, %(amount)s, %(date_payment)s);
        """
        prev_amount = None
        if amount < Config.limit:
            return None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel_id_driver, {"id_telegram": id_telegram})
            id_driver = cur.fetchone()[0]
            cur.execute(sql_sel_id_payment, {"id_driver": id_driver,
                                             "date_payment": date.strftime("%Y-%m-%d")})
            resp = cur.fetchone()
            if resp is not None:
                prev_amount = resp[0]
            else:
                prev_amount = -1
                try:
                    cur.execute(sql_ins_payments, {"id_driver": id_driver,
                                                   "amount": amount,
                                                   "date_payment": date.strftime("%Y-%m-%d")})
                except Error:
                    logger.exception("[WTF?]")
                else:
                    conn.commit()
        finally:
            cur.close()
            conn.close()

        return prev_amount

    def get_balance(self, id_telegram):
        sql = """
            SELECT `id_yataxi` FROM `drivers` WHERE `id_driver` IN 
            (SELECT `id_driver` FROM `telegrams` WHERE `id_telegram` = %(id)s) 
        """
        balance = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql, {"id": id_telegram})
            resp = cur.fetchone()
            if resp is not None:
                balance = int(Taximeter_api.get_balance(Config.token_taximeter, resp[0]))
            else:
                balance = 0
        finally:
            cur.close()
            conn.close()

        return balance

    def is_reg(self, id_telegram):
        sql = """
            SELECT `id_driver` FROM `telegrams` WHERE `id_telegram` = %(id)s 
        """
        reg = False
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql, {"id": id_telegram})
            resp = cur.fetchone()
            if resp is not None:
                if resp[0] is not None:
                    reg = True
        finally:
            cur.close()
            conn.close()
        return reg

    def get_statement(self, date, amount_on_account):
        sql_sel = """
            SELECT drivers.last_name, drivers.first_name, drivers.surname,
                zp_alfa.account_number, payments.amount, payments.id_payment, drivers.id_yataxi
            FROM drivers, payments, zp_alfa
            WHERE payments.date_payment = %(date)s
                AND payments.id_driver = zp_alfa.id_driver
                AND payments.id_driver = drivers.id_driver
            ORDER by payments.id_payment;
        """
        sql_upd = """
            UPDATE `payments`
            SET
                `amount` = %(amount)s
            WHERE 
                `id_payment` = %(id_payment)s
        """
        sql_del = """
            DELETE FROM `payments`
            WHERE `id_payment` = %(id_payment)s
        """
        list_payments = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel, {"date": date})
            resp = cur.fetchall()
            if resp is not None:
                list_payments = resp
            sum = 0
            overflow = False
            delete_ids = list()
            update_id = None
            update_sum = None
            for i in range(len(list_payments)):
                if overflow:
                    delete_ids.append(list_payments[i][5])
                    list_payments.remove(list_payments[i])
                else:
                    sum += list_payments[i][4]
                    if sum > amount_on_account:
                        sum -= list_payments[i][4]
                        overflow = True
                        if amount_on_account - sum >= Config.limit:
                            update_id = list_payments[i][5]
                            update_sum = int((amount_on_account - sum) / Config.delta) * Config.delta
                        else:
                            delete_ids.append(list_payments[i][5])
                            list_payments.remove(list_payments[i])
            try:
                if update_id is not None:
                    cur.execute(sql_upd, {"amount": update_sum,
                                          "id_payment": update_id})
                    list_ = list(list_payments[-1])
                    list_[4] = update_sum
                    list_payments.remove(list_payments[-1])
                    list_payments.append(tuple(list_))
                for del_id in delete_ids:
                    cur.execute(sql_del, {"id_payment": del_id})

            except Error:
                logger.exception("[WTF?]")
            else:
                conn.commit()
        finally:
            cur.close()
            conn.close()
        return list_payments

    def get_money_amount(self, date):
        sql_sel_sum = """
            SELECT SUM(amount) FROM payments
            WHERE date_payment=%(date)s;
        """
        sql_sel_lst = """
            SELECT drivers.last_name, drivers.first_name, drivers.surname, payments.amount
            FROM drivers, payments
            WHERE payments.date_payment = %(date)s
                AND payments.id_driver = drivers.id_driver
            ORDER by payments.id_payment;
        """
        money_amount = 0
        list_payments = []
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel_lst, {"date": date})
            resp = cur.fetchall()
            if resp is not None:
                list_payments = resp
                # money_amount = resp[0]
        finally:
            cur.close()
            conn.close()
        # return money_amount
        return list_payments

    def get_name(self, id_telegram):
        sql_sel = """
            SELECT `last_name`, `first_name`, `surname`, `id_driver` FROM `drivers` WHERE `id_driver` IN
            (SELECT `id_driver` FROM `telegrams` WHERE `id_telegram` = %(id_telegram)s);
        """
        response = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql_sel, {"id_telegram": id_telegram})
            resp = cur.fetchone()
            if resp is not None:
                response = " ".join([resp[0], resp[1], resp[2]]).upper()
        return response

    def test(self):
        sql = """
            SELECT `id_yataxi` FROM `yataxis` WHERE NOT`id_driver`=272;
        """
        reg = None
        try:
            conn = MySQLConnection(**self._dbconfig)
            cur = conn.cursor()
        except Error:
            logger.exception("[WTF?]")
        else:
            cur.execute(sql)
            resp = cur.fetchall()
            if resp is not None:
                reg = resp
        finally:
            cur.close()
            conn.close()
        return reg
