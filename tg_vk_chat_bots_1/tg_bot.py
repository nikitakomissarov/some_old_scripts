import json
import logging
from logging.handlers import TimedRotatingFileHandler
from dotenv import dotenv_values
from functools import partial
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from intent_detection import detect_intent_texts
from logger import TelegramLogsHandler, logger_bot


config = dotenv_values('.env')
TG_TOKEN = config['TG_TOKEN']
GOOGLE_APPLICATION_CREDENTIALS = config['GOOGLE_APPLICATION_CREDENTIALS']

logger_info = logging.getLogger('loggerinfo')
logger_error = logging.getLogger("loggererror")


async def start(update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.reply_text("The bot's been started")
    except Exception:
        logger_error.exception('Error')


async def reply(project_id, update, context: ContextTypes.DEFAULT_TYPE):
    try:
        language_code = update.message.from_user.language_code
        text = update.message.text
        session_id = update.message.chat.id
        google_reply = detect_intent_texts(
            project_id, session_id, text, language_code
        )
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=google_reply.fulfillment_text)
    except Exception:
        logger_error.exception('Error')


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

    try:
        with open(GOOGLE_APPLICATION_CREDENTIALS, "r") as google_file:
            credentials = google_file.read()
            credentials = json.loads(credentials)
            _, _, id_tuple, _, _ = credentials.items()
            _, project_id = id_tuple

        application = Application.builder().token(TG_TOKEN).build()

        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, partial(reply, project_id)))
        application.run_polling()

        logger_info.info("here we go")

    except Exception:
        logger_error.exception('Error')


if __name__ == '__main__':
    main()
