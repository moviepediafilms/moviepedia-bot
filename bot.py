import logging
from functools import wraps

from telegram.ext import Filters

from models.core import Movie, session as csession
from config import config

logger = logging.getLogger()

COMMANDS = {}

default_filter = Filters.chat(username=["zee_k"])


def command(*args, **kwargs):
    def wrapper(fn):
        @wraps(fn)
        def decorated(update, context):
            return fn(update, context)

        default_kwargs = {
            "filters": default_filter,
            "pass_args": True,
            "run_async": True,
        }
        if "filters" in kwargs:
            default_kwargs["filters"] = default_kwargs["filters"] & kwargs.pop(
                "filters"
            )
        default_kwargs.update(kwargs)
        COMMANDS[fn.__name__] = (fn, args, default_kwargs)
        return decorated

    return wrapper


@command()
def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
    )


@command()
def set_poster(update, context):
    text = ""

    try:
        movie_id = context.args[0]
        movie = csession.query(Movie).filter_by(id=int(movie_id)).first()
    except IndexError:
        text = "command should follow movie_id"
    else:
        text = f"selected movie: {movie.title}\ncurrent poster: {config.BASE_URL + movie.poster}\nsend a image to update poster in this movie"
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
