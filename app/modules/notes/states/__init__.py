from telegram.ext import MessageHandler, filters

from .start import start
from .note import note

from ..names import *


states = {
    NOTE: [MessageHandler(filters.TEXT | filters.PHOTO, note)]
}