import os


class BaseConfig:
    BOT_DATABASE_URL = os.environ["BOT_DATABASE_URL"]
    CORE_DATABASE_URL = os.environ["CORE_DATABASE_URL"]
    BOT_TOKEN = os.environ["BOT_TOKEN"]
    BASE_URL = os.environ["BASE_URL"]
    POSTER_PATH = os.environ["POSTER_PATH"]
    ADMINS = os.environ["ADMINS"]


config = BaseConfig()
