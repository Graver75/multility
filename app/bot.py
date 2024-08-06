import logging
import os
import asyncio
import json

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, Bot
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv

import helper

from db import DB
import models

from rabbitmq import RabbitMQClient


load_dotenv()

RABBITMQ_LOGIN = os.getenv('RABBITMQ_LOGIN')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')

MYSQL_LOGIN = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_HOST = os.getenv('MYSQL_HOST')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

TOKEN = os.getenv('BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text('Сюда будут сыпаться ошибки')

async def choose_module(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.message.from_user
    modules = helper.getModules()

    reply_keyboard = [
        [KeyboardButton(module)] for module in modules
    ]
    await update.message.reply_text(
        "Choose a module",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Choose a module"
        ),
    )

    return ConversationHandler.END

async def send_error_message(message):
    await message.ack()

    bot = Bot(TOKEN)

    message = message.body.decode()
    message = json.loads(message)

    if message['message'] and message['to_tg']:
        for chat_id in message['to_tg']:
            await bot.send_message(chat_id, message['message'])

def main() -> None:
    db = DB(MYSQL_LOGIN, MYSQL_PASSWORD, MYSQL_HOST, 'multility')

    models.create_tables()

    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
        },
        fallbacks=[],
    )

    # rabbitmq = RabbitMQClient(RABBITMQ_LOGIN, RABBITMQ_PASSWORD, RABBITMQ_HOST, [
    #     ('errors', send_error_message)
    # ])
    # asyncio.get_event_loop().create_task(rabbitmq.listen())

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()