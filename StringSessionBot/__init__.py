# StringSessionBot Plugin
# This file makes the directory a Pyrogram plugin

# Import all handlers to register them
from . import start
from . import generate
from . import callbacks
from . import help
from . import about
from . import bot_users
from . import must_join

# Plugin info
__version__ = "1.0.0"
__author__ = "String Session Bot"
__description__ = "Telegram bot for generating Pyrogram and Telethon string sessions" 