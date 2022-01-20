import datetime
import logging
import csv

from MenuBot import MenuBot
from telebot import types

import Database
import Taximeter_api
import Message_texts
import Config
import Excel

from Config import token_taximeter
from Config import logger
import os

db = Database.DataBase()
bot = MenuBot(Config.token_drivers_bot)
# bot = MenuBot(Config.test_token)


def _reduce_balances(list_payments, lst_suc=0):
    logger.info("reduce balance, length: %d", len(list_payments))
    logger.debug("last success %d", lst_suc)
    last_success_req = None
    for i in range(lst_suc, len(list_payments)):
        # resp = 200
        resp = Taximeter_api.reduce_balance(token_taximeter, list_payments[i][6],
                                            int(list_payments[i][4] * Config.commission))
        logger.info("{} {}".format(resp, list_payments[i]))
        if resp != 200:
            last_success_req = i - 1
            break
    return last_success_req


def _get_drivers_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(Message_texts.get_paid)
    keyboard.add(Message_texts.request_balance)
    # keyboard.add(Message_texts.taximania)
    return keyboard


def _get_dispatchs_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(Message_texts.get_money_amount)
    keyboard.add(Message_texts.get_statement_file)
    keyboard.add(Message_texts.set_alfabank_list)
    keyboard.add(Message_texts.set_taximania)
    return keyboard


@bot.menu_handler("driver", "Меню водителя\nПодписывайся на канал https://t.me/yataxistmsk", _get_drivers_keyboard())
def handle_driver(message):
    logger.debug("{0} sent /driver".format(message.chat.id))
    if db.is_reg(message.chat.id):
        return True
    else:
        bot.send_message(chat_id=message.chat.id,
                         text="Вы еще не зарегистрированы\n"
                              "Введите /reg",
                         reply_markup=types.ReplyKeyboardRemove())
        return False


@bot.menu_handler("dispatch", "Меню диспетчера", _get_dispatchs_keyboard())
def handle_dispatch(message):
    logger.debug("{0} sent /dispatch".format(message.chat.id))
    if message.chat.id in Config.dispatchs:
        return True
    else:
        return False


def _get_moneys_keyboard(sum):
    keyboard = types.InlineKeyboardMarkup()
    if sum <= 5000:
        itr = range(Config.limit, sum + 1, 500)
    else:
        itr = range(Config.limit, 5000 + 1, 500)
    row = []
    for i in itr:
        row.append(types.InlineKeyboardButton(str(i), callback_data=str(i)))
        if len(row) >= 2:
            keyboard.row(*row)
            row = []
    if len(row) == 1:
        row.append(Message_texts.other_amount)
        keyboard.row(*row)
    elif len(row) == 0:
        keyboard.add(Message_texts.other_amount)
    return keyboard


def is_working_time(date_time):
    
    #!!!!!!!
    #return False
    #!!!!!!!
    time = datetime.time(hour=date_time.hour,
                         minute=date_time.minute)
    if Config.working_time_start <= time <= Config.working_time_end:
        if Config.calend is not None:
            dic = Config.calend.get(date_time.year)
            if dic is not None:
                if date_time.day in dic[date_time.month]:
                    return False
                else:
                    return True
        if 0 <= date_time.weekday() <= 4:
            return True
    else:
        return False


def add_paid(id, amount):
    balance = db.get_balance(id)
    if (amount >= Config.limit) and (amount <= int(balance * Config.commission)):
        prev_amount = db.add_payments(id, amount, datetime.date.today())
        if prev_amount is None:
            pass
        elif prev_amount < 0:
            logger.info("{0} add paid, amount: {1}".format(id, amount))
            return "Запрос на вывод {} руб. принят\n" \
                   "Деньги будут списаны со счёта в таксометре" \
                   " и отправлены на карту Альфа-Банка сегодня с 17 до 19 часов.".format(amount)
        else:
            return "Сегодня Вы уже запросили {} руб".format(prev_amount)
    else:
        return "Недоступно\nВаш баланс: {}\nМинимальная сумма вывода: {}".format(balance, Config.limit)


@bot.message_handler(commands=["start", "help"])
def handle_start_help(message):
    logger.debug("{0} sent /start".format(message.chat.id))
    bot.send_message(chat_id=message.chat.id,
                     text=Message_texts.start_help)

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(Message_texts.shareNumber, request_contact=True))
    msg = bot.send_message(chat_id=message.chat.id,
                           text=Message_texts.registration,
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_contact)


@bot.message_handler(commands=["stop"])
def handle_stop(message):
    logger.debug("%d sent /stop" % message.chat.id)
    if message.chat.id in Config.admins:
        bot.save()
        bot.stop_polling()


@bot.message_handler(commands=["reg"])
def handle_reg(message):
    logger.info("Sent a request for registration to {0}".format(message.chat.id))
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton(Message_texts.shareNumber, request_contact=True))
    msg = bot.send_message(chat_id=message.chat.id,
                           text=Message_texts.registration,
                           reply_markup=keyboard)
    bot.register_next_step_handler(msg, handle_contact)


def handle_contact(message):
    if message.contact is not None:
        logger.info(message.contact)
        if message.from_user.id == message.contact.user_id:
            phone = message.contact.phone_number
            if not phone.startswith("+"):
                phone = "+" + phone

            bot.driverPhone = phone
            name = db.add_telegram_driver(phone=phone, id_telegram=message.chat.id)
            if name is not None:
                logger.info("registration is correct for {} '{}'".format(message.chat.id, name))
                bot.send_message(chat_id=message.chat.id,
                                 text=Message_texts.registrationCorrect % name,
                                 reply_markup=types.ReplyKeyboardRemove())
                bot.send_menu(message, command="driver")
            else:
                logger.info("registration is incorrect for {} '{}'".format(message.chat.id, name))
                '''bot.send_message(chat_id=message.chat.id,
                                 text=Message_texts.registrationIncorrect,
                                 reply_markup=types.ReplyKeyboardRemove())'''
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                keyboard.add(types.InlineKeyboardButton("Зарегестрироваться в таксопарке", callback_data="driver"))
                msg = bot.send_message(chat_id=message.chat.id,
                                       text=Message_texts.registrationIncorrect,
                                       reply_markup=keyboard)
                bot.register_next_step_handler(msg, handle_driver)


        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton(Message_texts.shareNumber, request_contact=True))
            msg = bot.send_message(chat_id=message.chat.id,
                             text="Вы отправили не свой телефон",
                             reply_markup=keyboard)
            bot.register_next_step_handler(msg, handle_contact)
    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton(Message_texts.shareNumber, request_contact=True))
        msg = bot.send_message(chat_id=message.chat.id,
                         text="Вы не отправили телефон",
                         reply_markup=keyboard)
        bot.register_next_step_handler(msg, handle_contact)

def handle_driver(message):
    bot.registerInPark = True
    bot.send_message(chat_id=message.chat.id,
                     text="Отправьте скан паспорта",
                     reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(content_types=["photo"])
def downloadPhoto(message):
    if bot.registerInPark:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        path = os.getcwd()

        if not os.path.exists(path + '/' + bot.driverPhone):
            os.mkdir(path + '/' + bot.driverPhone)

        num_files = len([f for f in os.listdir(path + '/' + bot.driverPhone)
                         if os.path.isfile(os.path.join(path + '/' + bot.driverPhone, f))])
        if num_files <= 2:
            if num_files <= 1:
                src = path + '/' + bot.driverPhone + '/pass.jpg'
            else:
                src = path + '/' + bot.driverPhone + '/driverLicense.jpg'

            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            bot.reply_to(message, "Фото добавлено")
            if num_files <= 1:
                bot.send_message(chat_id=message.chat.id,
                                 text="Отправьте скан водительских прав",
                                 reply_markup=types.ReplyKeyboardRemove())
            else:
                bot.send_message(chat_id=message.chat.id,
                                 text="Спасибо, данные переданы менеджеру",
                                 reply_markup=types.ReplyKeyboardRemove())



@bot.callback_query_handler(func=lambda callback: callback.data == Message_texts.get_paid.callback_data)
def handle_callback_get_paid(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data="driver"))
    if is_working_time(datetime.datetime.now()):
        balance = db.get_balance(callback.message.chat.id)
        status = db.available(callback.message.chat.id)
        if status == "Не заказана":
            bot.send_menu(callback.message,
                          command="driver",
                          text="Недоступно\nСтатус вашей карты:\n{}\n Обратитесь в офис для заказа карты".format(status),
                          keyboard=keyboard)
        elif balance < int(Config.limit * Config.commission):
            bot.send_menu(callback.message,
                          command="driver",
                          text="Недоступно, ваш баланс: {}\nМинимальная сумма вывода: {}".format(balance, Config.limit),
                          keyboard=keyboard)
        else:
            keyboard = _get_moneys_keyboard(balance)
            keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data="driver"))
            bot.send_menu(callback.message,
                          command="driver",
                          text="Ваш баланс: {}\nВыберите сумму".format(balance),
                          keyboard=keyboard)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(types.KeyboardButton('Моментальная выплата (500 - 5000)'))
            keyboard.add(types.KeyboardButton('Моментальная выплата (2000 - 5000)'))
    else:
        bot.send_menu(callback.message,
                      command="driver",
                      #text="Недоступно, в нерабочее время\n",
                      text="Вывод средств через бота приостановлен\n",
                      keyboard=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data.isdigit())
def handle_callback_digit_amount(callback):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data="driver"))
    bot.send_menu(callback.message,
                  command="driver",
                  text=add_paid(id=callback.message.chat.id, amount=int(callback.data)),
                  keyboard=keyboard)


def enter_other_amount(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data="driver"))
    if message.text.isdigit():
        bot.send_menu(message,
                      command="driver",
                      text=add_paid(id=message.chat.id, amount=int(message.text)),
                      keyboard=keyboard)
    else:
        bot.send_menu(message,
                      command="driver",
                      text="Вы ввели не число",
                      keyboard=keyboard)


@bot.callback_query_handler(func=lambda callback: callback.data == Message_texts.other_amount.callback_data)
def handle_callback_other_amount(callback):
    balance = db.get_balance(callback.message.chat.id)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data="driver"))
    msg = bot.send_menu(callback.message,
                        command="driver",
                        text="Ваш баланс: {}\n{}".format(balance, Message_texts.enterAmount),
                        keyboard=keyboard)
    bot.register_next_step_handler(msg, enter_other_amount)

# @bot.button_handler(Message_texts.taximania.callback_data)
def handle_callback_taximania(callback):
    name = db.get_name(callback.message.chat.id)
    # name = "Абабков Николай Борисович"
    # name = name.upper()
    list_taximania = []
    strin = "Ваше место: {}\nВыполнено заказаов: {}\n\nТоп 10:\nФИО                      Заказы\n"
    with open(Config.taximania.format("24-01-2018.csv"), "r", encoding="windows-1251") as file:
        reader = csv.reader(file, delimiter=";")
        i = 0
        you_score = []
        found = False
        for row in reader:
            i += 1
            if i <= 10:
                tmp = "{}  {}\n".format(row[0], row[1])
                strin += tmp
            if not found:
                if row[0].upper() == name:
                    found = True
                    you_score = [str(i), str(row[1])]
            if found and i > 10:
                break
        if not found:
            you_score = ["> "+str(i), str(0)]
        return strin.format(*you_score)

    # for it in list_taximania:
    #     print(it)


@bot.button_handler(Message_texts.request_balance.callback_data)
def handle_callback_balance(callback):
    balance = db.get_balance(callback.message.chat.id)
    return "Ваш баланс: {}".format(balance)


@bot.button_handler(Message_texts.get_money_amount.callback_data)
def handle_callback_money_amount(callback):
    lst = db.get_money_amount(datetime.date.today())
    strin = "Водители запросили {} руб.\n"
    money_amount = 0
    for row in lst:
        money_amount += row[3]
        strin += " ".join([row[0], row[1], row[2]]).upper() + " " + str(row[3]) + "\n"
    return strin.format(money_amount)


def set_alfabank_file(message):
    if message.document is None:
        return "Вы не прикрепили файл"
    elif message.document.file_name.endswith(".txt"):
        file_ = bot.download_file(bot.get_file(message.document.file_id).file_path)
        fl = file_.decode('utf-8').replace("\t\t", ";").replace("Закрыт\r\n", " Закрыт;").replace("\r\n4", "4") \
            .replace("\n\t", "\n").replace("\t", ";").replace("\n\n", "\n").strip()
        try:
            file = open(Config.alfabank_file, "w")
            if fl[1] == ";":
                file.write(fl[2:])
            else:
                file.write(fl)
            return "Данные обновяться в 1:00"
        except OSError:
            return "Не удалось сохранить файл"
    else:
        return "Неверный тип файла"


@bot.button_handler(Message_texts.set_alfabank_list.callback_data, set_alfabank_file)
def handle_callback_set_alfabank(callback):
    logger.info("{0} set alfabank".format(callback.message.chat.id))
    return "Отправьте файл с данными"


def set_money_on_account(message):
    time_end = datetime.time(hour=23, minute=45)
    time = datetime.time(hour=datetime.datetime.now().hour,
                         minute=datetime.datetime.now().minute)
    '''if not (Config.working_time_end < time < time_end):
        return "Еще не закончилось время приема заявок"'''
    if message.text.isdigit():
        return get_statement(message, int(message.text))
    else:
        return "Вы ввели не число"


@bot.button_handler(Message_texts.get_statement_file.callback_data, set_money_on_account)
def handle_callback_statement_file(callback):
    return "Введите сколько денег на счету"


def get_statement(message, money):
    logger.info("{0} get statement".format(message.chat.id))
    list_statement = db.get_statement(datetime.date.today(), money)
    flag = 1
    lst_suc = _reduce_balances(list_statement, 0)
    while lst_suc is not None:
        if flag > 5:
            break
        flag += 1
        lst_suc = _reduce_balances(list_statement, lst_suc)
    statement_file = Excel.create_statement(Config.template_file_xls, list_statement)
    with open(statement_file, "rb") as file:
        bot.send_document(message.chat.id, file)
    return "Файл отправлен"


def set_taximania(message):
    if message.document is None:
        return "Вы не прикрепили файл"
    elif message.document.file_name.endswith(".csv"):
        file_ = bot.download_file(bot.get_file(message.document.file_id).file_path)
        try:
            print(message.document.file_name)
            file = open(Config.taximania.format(message.document.file_name), "wb")
            file.write(file_)
            return "Файл успешно принят"
        except OSError as err:
            print(err)
            return "Не удалось сохранить файл"
    else:
        return "Неверный тип файла"


@bot.button_handler(Message_texts.set_taximania.callback_data, set_taximania)
def handle_callback_set_taximania(callback):
    logger.info("{0} set taximania".format(callback.message.chat.id))
    return "Отправте файл с данными"


def main():
    logger.setLevel(logging.DEBUG)
    try:
        bot.polling(none_stop=True)
    except Exception:
        logger.exception("WTF?")
    finally:
        bot.save()


if __name__ == "__main__":
    main()
