import json
from json import JSONDecodeError
from os import path
from collections import defaultdict
from telebot import TeleBot
from telebot.apihelper import ApiException
from telebot.types import InlineKeyboardMarkup


class MyBot(TeleBot):
    def __init__(self, token):
        TeleBot.__init__(self, token)
        self._filename = path.join(path.dirname(__file__), ".{}.json".format(self.token[:9]))
        self.chats_data = defaultdict(lambda: {"last_id": 0, "menu_id": 0, "state": 0})
        # self.chats_data = defaultdict(int)
        self._load()

    def _load(self):
        def _json_keys_to_int(unk):
            if isinstance(unk, dict):
                return {int(k) if k.isdigit() else k: v for k, v in unk.items()}
            return unk
        lst = [0, {}, {}]
        try:
            file = open(self._filename, encoding="utf-8")
            lst = json.load(file, object_hook=_json_keys_to_int)
            self.last_update_id = lst[0]
            self.message_subscribers_next_step = lst[1]
            self.chats_data.update(lst[2])
        except (FileNotFoundError, JSONDecodeError, KeyError):
            with open(self._filename, 'w', encoding="utf-8") as file:
                file.write(json.dumps(lst, ensure_ascii=False))

    def save(self):
        self._append_pre_next_step_handler()
        try:
            file = open(self._filename, 'w', encoding="utf-8")
            lst = [self.last_update_id, self.message_subscribers_next_step, self.chats_data]
            file.write(json.dumps(lst, ensure_ascii=False))
            # logger.info("saved '_last_ids'")
            file.close()
            return True
        except OSError:
            return False

    def process_new_messages(self, messages):
        for message in messages:
            self.chats_data[message.chat.id]["last_id"] = message.message_id
        TeleBot.process_new_messages(self, messages)

    def send_menu(self, chat_id, text, reply_markup=None, disable_web_page_preview=None, parse_mode=None):
        menu_id = self.chats_data[chat_id]["menu_id"]
        last_id = self.chats_data[chat_id]["last_id"]
        if last_id <= menu_id:
            try:
                msg = self.edit_message_text(text, chat_id, menu_id, None, parse_mode,
                                             disable_web_page_preview, reply_markup)
                return msg
            except ApiException:
                pass
        try:
            self.edit_message_reply_markup(chat_id, menu_id, None, InlineKeyboardMarkup())
        except ApiException:
            pass
        msg = self.send_message(chat_id, text, disable_web_page_preview, None, reply_markup, parse_mode, True)
        self.chats_data[chat_id]["menu_id"] = msg.message_id
        self.chats_data[chat_id]["last_id"] = msg.message_id
        return msg
