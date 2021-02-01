from sqlalchemy import create_engine, Column, ForeignKey, Integer, String, Text, Table
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import config

Base = declarative_base()
engine = create_engine(config.BOT_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True)


class Command(Base):
    __tablename__ = "command"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user = Column(Integer, ForeignKey("user.username"))
    command = Column(String)
    state = Column(String)
