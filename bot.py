import os
import logging
import time
from functools import wraps
import shutil

from telegram.ext import Filters

from models.core import Movie, Session as CoreSession
from config import config

logger = logging.getLogger()

COMMANDS = {}

default_filter = Filters.chat(username=config.ADMINS.split(","))


def get_post_name(movie_id):
    return str(movie_id).rjust(10, "0") + ".png"


def command(*args, **kwargs):
    def wrapper(fn):
        @wraps(fn)
        def decorated(update, context):
            return fn(update, context)

        default_kwargs = {
            "filters": default_filter,
            "pass_args": True,
            "run_async": False,
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


def _get_poster_photo(message):
    photo = next(
        (photo for photo in message.photo if (photo.width, photo.height) == (289, 512)),
        None,
    )
    if not photo:
        return
    file = photo.get_file()
    file_path = file.download(
        os.path.join("posters", f"{int(time.time())}.png"), timeout=100
    )
    logger.info(f"file saved at {file_path}")
    return file_path


def _set_poster(poster_path, movie_id):
    """
    - movie the poster image from poster_path to media path along with other posters
    - update database to set new poster path if its not already there

    Args:
        poster_path (str): string path of poster file referenced by sender
        movie_id (int): pk of movie
    """
    src_poster = os.path.join(".", poster_path)
    dest_poster = os.path.join(config.POSTER_PATH, get_post_name(movie_id))
    shutil.move(src_poster, dest_poster)
    logger.info(
        f"move {poster_path} to {config.POSTER_PATH}/{str(movie_id).rjust(10, '0')}.png"
    )


def _update_movie(movie_id, core_session):
    movie = core_session.query(Movie).filter_by(id=movie_id).first()
    if not movie.poster:
        movie.poster = "/media/posters/" + get_post_name(movie_id)
        core_session.commit()


@command()
def set_poster(update, context):
    text = ""
    try:
        core_session = CoreSession()
        movie_id = context.args[0]
        movie = core_session.query(Movie).filter_by(id=int(movie_id)).first()
    except IndexError:
        text = "missing movie ID! usage: reply to an image with '/set_poster <movie_id>' to update poster for a movie"
    except Exception as ex:
        text = str(ex)
    else:
        if not movie:
            text = "no such movie exists"
        else:
            if not update.effective_message.reply_to_message:
                text = "reply to a photo message to set poster"
            else:
                poster_path = _get_poster_photo(
                    update.effective_message.reply_to_message
                )
                if not poster_path:
                    text = "You have to reply to a image with dimensions 289, 512"
                else:
                    _set_poster(poster_path, movie_id)
                    _update_movie(movie_id, core_session)
                    text = f"Poster updated for '{movie.title}'\nNew poster at: {config.BASE_URL + movie.poster}"
    finally:
        core_session.close()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text)
