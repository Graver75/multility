from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from ..names import *


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Ага')

    reply_keyboard = [['Сохранить']]
    await update.message.reply_text(
        "Нажмите кнопку 'Сохранить', когда закончите:",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
    )

    return NOTE
