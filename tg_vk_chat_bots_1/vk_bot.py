﻿import random
import logging
from logging.handlers import TimedRotatingFileHandler
import json
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import dotenv_values
from intent_detection import detect_intent_texts
from logger import TelegramLogsHandler, logger_bot


config = dotenv_values('.env')
VK_TOKEN = config['VK_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']

logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")


def reply(event, vk, project_id):
    language_code = 'ru'
    text = event.text
    session_id = event.peer_id
    google_reply = detect_intent_texts(project_id,
                                       session_id, text, language_code)
    if not google_reply.intent.is_fallback:
        vk.messages.send(
            user_id=event.user_id,
            message=google_reply.fulfillment_text,
            random_id=random.randint(1, 1000)
        )


def handle_vk_events(longpoll, vk, project_id):
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply(event, vk, project_id)


def main():
    handler = TimedRotatingFileHandler("app.log", when='D', interval=30, backupCount=1)
    handler_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(handler_format)
    logger_info.setLevel(logging.INFO)
    logger_info.addHandler(handler)
    logger_error.setLevel(logging.ERROR)
    logger_error.addHandler(handler)
    telegram_notification_handler = TelegramLogsHandler(logger_bot)
    telegram_notification_handler.setFormatter(handler_format)
    logger_error.addHandler(telegram_notification_handler)

    while True:
        try:
            with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as google_file:
                credentials = google_file.read()
                credentials = json.loads(credentials)
                _, _, id_tuple, _, _ = credentials.items()
                _, project_id = id_tuple

            vk_session = vk_api.VkApi(token=VK_TOKEN)
            longpoll = VkLongPoll(vk_session)
            vk = vk_session.get_api()

            logger_info.info("here we go")
            handle_vk_events(longpoll, vk, project_id)

        except Exception:
            logger_error.exception('Error')


if __name__ == '__main__':
    main()
