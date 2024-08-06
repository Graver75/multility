from telegram.ext import MessageHandler, filters

from .start import start
from .note import note
from .title import title

from ..names import *


states = {
    NOTE: [MessageHandler(filters.TEXT | filters.PHOTO, note)],
    TITLE: [MessageHandler(filters.TEXT, title)],
}