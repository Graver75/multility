from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup, KeyboardButton

from ..names import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Ага')

    reply_keyboard = [['Сохранить']]
    await update.message.reply_text(
        "Введи название заметки:",
    )

    return TITLE
