from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup, KeyboardButton

from ..names import *

from app.models.Note import Note
from app.models.User import User

from app.db import db

from app.bot import start


async def send(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = update.message.text
    title = text.replace('[', '').replace(']', '')

    session = db.get_session()

    user = session.query(User).filter_by(chat_id=update.message.from_user.id).first()
    notes = session.query(Note).filter_by(title=title).all()

    for note in notes:
        if note.type == 'text':
            await update.message.reply_text(note.content)
        elif note.type == 'photo':
            await update.message.reply_photo(note.content)

    return await start(update, context)


async def title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    notes_title = update.message.text
    if notes_title.startswith('[[') and notes_title.endswith(']]'):
        return await send(update, context)
    reply_keyboard = [['Сохранить']]
    await update.message.reply_text(
        f"Введи содержимое заметки {notes_title}",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Название", resize_keyboard=True
        ),
    )

    context.chat_data['new_note'] = {}
    context.chat_data['new_note']['title'] = notes_title

    return NOTE