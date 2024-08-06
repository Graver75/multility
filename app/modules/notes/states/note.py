from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from ..names import *


async def note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    await update.message.reply_text('Угу')
