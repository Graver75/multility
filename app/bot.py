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

import db

from app.models import User

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

logging.basicConfig(
    filename='bot.log',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


Base = db.db.Base
session = db.db.get_session()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    user = update.message.from_user
    chat_id = user.id
    name = user.username or user.first_name or 'Anonymous'

    existing_user = session.query(User).filter_by(chat_id=chat_id).first()

    if not existing_user:
        user = User(name=name, chat_id=chat_id)
        session.add(user)
        session.commit()
        logging.info(f'New user {name} {chat_id} added to the database')
        await update.message.reply_text('Вроде записал тебя, хз')

    return await choose_module(update, context)


async def choose_module(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    modules = helper.get_modules()

    reply_keyboard = [
        [KeyboardButton(module)] for module in modules
    ]
    await update.message.reply_text(
        "Выбери модуль:",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Модуль", resize_keyboard=True
        ),
    )

    return 'module_chosen'


async def to_module(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    chosen_module = update.message.text
    module_start = helper.get_module_start(chosen_module)
    return await module_start(update, context)


async def send_error_message(message):
    await message.ack()

    bot = Bot(TOKEN)

    message = message.body.decode()
    message = json.loads(message)

    if message['message'] and message['to_tg']:
        for chat_id in message['to_tg']:
            await bot.send_message(chat_id, message['message'])


def main() -> None:
    db.db.create_tables()

    application = Application.builder().token(TOKEN).build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            'module_chosen': [MessageHandler(filters.TEXT & ~filters.COMMAND, to_module)],
        },
        fallbacks=[],
    )

    modules = helper.get_modules()
    for module in modules:
        module_states = helper.get_module_states(module)
        conv_handler.states.update(module_states)

    # rabbitmq = RabbitMQClient(RABBITMQ_LOGIN, RABBITMQ_PASSWORD, RABBITMQ_HOST, [
    #     ('errors', send_error_message)
    # ])
    # asyncio.get_event_loop().create_task(rabbitmq.listen())

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()