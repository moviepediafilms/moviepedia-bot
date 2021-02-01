import os
import logging

from telegram.ext import CommandHandler, Updater


from bot import COMMANDS
from config import config

logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()

updater = Updater(token=config.BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher


def init_db():
    from models.bot import Base, engine
    Base.metadata.create_all(engine)


def register_commands():
    for name, value in COMMANDS.items():
        fn, args, kwargs = value
        logger.debug(
            f"registering command:  CommandHandler({name}, <fn>, *{args}, **{kwargs})"
        )
        dispatcher.add_handler(CommandHandler(name, fn, *args, **kwargs))


init_db()
register_commands()
updater.start_polling()
