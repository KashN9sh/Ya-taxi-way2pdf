import json
import os
from json.decoder import JSONDecodeError

import telebot
from telebot import types
from telebot import logger


def jsonKeys2str(x):
    if isinstance(x, dict):
        return {int(k) if k.isdigit() else k : v for k, v in x.items()}
    return x


class MenuBot(telebot.TeleBot):
    driverPhone = ''
    registerInPark =False
    def __init__(self, token):
        super().__init__(token)
        self.filename = os.path.join(os.path.dirname(__file__), ".{}_last_ids.json".format(self.token.split(':')[0]))
        self.remove_webhook()
        self._command_menu = dict()
        self._last_ids = self._load()

    def decorator(self, func, command):
        def wrapper(message):
            keyboard = types.InlineKeyboardMarkup()
            retr = func(message)
            if isinstance(retr, str):
                text = retr
            elif isinstance(retr, tuple):
                text = retr[0]
                if len(retr) > 1:
                    keyboard = retr[1]
            keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data=command))
            self.send_menu(message, command, text, keyboard)
        return wrapper

    def _load(self):
        resp = dict()
        try:
            file = open(self.filename, encoding="utf-8")
            resp = json.load(file,  object_hook=jsonKeys2str)
        except (FileNotFoundError, JSONDecodeError):
            with open(self.filename, 'w', encoding="utf-8") as file:
                file.write(json.dumps(resp, ensure_ascii=False))
        return resp

    def _back_to_menu(self, callback):
        #self.pre_message_subscribers_next_step[callback.message.chat.id] = []
        self.send_menu(callback.message, command=callback.data)

    def process_new_messages(self, messages):
        for message in messages:
            self._last_ids.setdefault(message.chat.id, dict())["msg"] = message.message_id
            self._last_ids[message.chat.id].setdefault("menu", 0)
        super().process_new_messages(messages)

    def save(self):
        try:
            file = open(self.filename, 'w', encoding="utf-8")
            file.write(json.dumps(self._last_ids, ensure_ascii=False))
            logger.info("saved '_last_ids'")
            logger.debug(self._last_ids)
            file.close()
            return True
        except OSError:
            return False

    def _bind_button(self, func, cb_data):
        class Test():
            data = cb_data
        for i in self.callback_query_handlers:
            if i["filters"]["func"](Test()):
                i["function"] = func
                return
        handler_dict = self._build_handler_dict(func,
                                                func=lambda callback: callback.data == cb_data)
        self.add_callback_query_handler(handler_dict)

    def button_handler(self, callback_data, next_handler=None):
        command = None
        for i in self._command_menu:
            for row in self._command_menu[i]["keyboard"].keyboard:
                for button in row:
                    if button.callback_data == callback_data:
                        command = i
        if command is None:
            raise LookupError("'{}' is not in data created button".format(callback_data))

        def decorator(func):
            def wrapper(callback):
                keyboard = types.InlineKeyboardMarkup()
                retr = func(callback)
                if isinstance(retr, str):
                    text = retr
                elif isinstance(retr, tuple):
                    text = retr[0]
                    if len(retr) > 1:
                        keyboard = retr[1]
                keyboard.add(types.InlineKeyboardButton("Вернуться", callback_data=command))
                msg = self.send_menu(callback.message, command, text, keyboard)
                if next_handler is not None:
                    self.register_next_step_handler(msg, self.decorator(next_handler, command))
            self._bind_button(wrapper, callback_data)
            return wrapper

        return decorator

    def menu_handler(self, command, text, keyboard):
        logger.debug("add menu command '{}', text '{}', keyboard '{}'", command, text, keyboard)
        if command in self._command_menu:
            raise ValueError("duplicate command '{}'".format(command))
        self._command_menu[command] = dict()
        self._command_menu[command]["text"] = text
        self._command_menu[command]["keyboard"] = keyboard

        def decorator(func):
            def wrapper(message):
                if func(message):
                    self.send_menu(message, command)
            handler_dict = self._build_handler_dict(wrapper,
                                                    commands=[command])
            self.add_message_handler(handler_dict)
            return wrapper
        self._bind_button(self._back_to_menu, command)
        return decorator

    def send_menu(self, message, command=None, text=None, keyboard=None, disable_notification=None):
        logger.debug("send menu to {} command '{}'", message.chat.id, command)
        if text is None:
            text = self._command_menu[command]["text"]
        if keyboard is None:
            keyboard = self._command_menu[command]["keyboard"]
        last_id = self._last_ids[message.chat.id]["menu"]
        if self._last_ids[message.chat.id]["msg"] > last_id:
            msg = self.send_message(chat_id=message.chat.id,
                                    text=text,
                                    reply_markup=keyboard,
                                    disable_notification=disable_notification)
            try:
                self.delete_message(msg.chat.id, last_id)
            except telebot.apihelper.ApiException:
                pass
            self._last_ids[message.chat.id]["menu"] = msg.message_id
        else:
            msg = self.edit_message_text(text, message.chat.id, last_id, reply_markup=keyboard)
        return msg
