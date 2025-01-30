import telebot
from loguru import logger

import settings


class TelegramService:
    @staticmethod
    def send_msg(msg: str):
        try:
            bot = telebot.TeleBot(settings.tg_token)
            bot.send_message(settings.tg_id, msg, parse_mode="html")
        except Exception as error:
            logger.error(error)
