from telebot.types import InlineKeyboardButton

get_paid = InlineKeyboardButton(text="Вывод денег",
                                callback_data="money")
request_balance = InlineKeyboardButton(text="Показать баланс",
                                       callback_data="balance")
taximania = InlineKeyboardButton(text="Таксимания",
                                 callback_data="taximania")
other_amount = InlineKeyboardButton(text="Другая сумма",
                                    callback_data="other_amount")
back_to_drivers_menu = InlineKeyboardButton(text="Вернуться в меню",
                                            callback_data="back_to_drivers_menu")

get_money_amount = InlineKeyboardButton(text="Сколько денег запросили",
                                        callback_data="get_money_amount")
get_statement_file = InlineKeyboardButton(text="Получить отчет",
                                          callback_data="get_statement")
set_alfabank_list = InlineKeyboardButton(text="Обновить файл",
                                         callback_data="set_alfabank")
set_taximania = InlineKeyboardButton(text="Файл Таксимании",
                                     callback_data="set_taximania")
back_to_dispatchs_menu = InlineKeyboardButton(text="Вернуться в меню",
                                              callback_data="back_to_admins_menu")

dispatchs_menu = "Меню диспетчера"

order = InlineKeyboardButton(text="Заказать",
                             callback_data="order")


enterAmount = "Введите сумму цифрами"
showBalance = "Ваш баланс %d"

shareNumber = "Да, отправить свой номер телефона"
register = "Зарегестрироваться в таксопарке"

start_help = """Привет,я бот для водителей компнии Я-Таксист.

"""

drivers_menu = "Меню водителя"
menuButton = "Меню"

registration = "Пожалуйста сообщите свой телефон\nДля этого нажмите внизу экрана кнопку:\n"+shareNumber
registrationCorrect = "Здравствуйте, %s"
registrationIncorrect = "Вы не являетесь водителем компании"
