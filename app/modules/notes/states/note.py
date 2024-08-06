import os

from telegram import Update
from telegram.ext import ContextTypes
from telegram import ReplyKeyboardMarkup, KeyboardButton
import asyncio

from ..names import *

from app.models.Note import Note
from app.models.User import User

from app.db import db

from app.bot import start

async def note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> str:
    text = update.message.text
    photo = update.message.photo

    session = db.get_session()

    user = session.query(User).filter_by(chat_id=update.message.from_user.id).first()

    if text:
        if text == 'Сохранить':
            return await start(update, context)

        note = Note(title=context.chat_data['new_note']['title'], type='text', content=text, user_id=user.id)
    else:
        photo = await photo[-1].get_file()
        save_dir = f'notes/{user.id}/{context.chat_data["new_note"]["title"]}'
        os.makedirs(save_dir, exist_ok=True)
        path = await photo.download_to_drive(f'notes/{user.id}/{context.chat_data["new_note"]["title"]}/{photo.file_unique_id}.jpg')
        note = Note(title=context.chat_data['new_note']['title'], type='photo', content=path, user_id=user.id)

    session.add(note)
    session.commit()

    await update.message.reply_text('Заметка добавлена')

    return NOTE