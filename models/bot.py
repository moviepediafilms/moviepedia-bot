import enum
from datetime import datetime

from sqlalchemy import (
    create_engine,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from config import config

Base = declarative_base()
engine = create_engine(config.BOT_DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# non model classes


# model classes
class User(Base):
    __tablename__ = "user"

    username = Column(String, primary_key=True)

    commands = relationship(
        "Command", back_populates="user", cascade="all, delete, delete-orphan"
    )


class Command(Base):
    __tablename__ = "command"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_username = Column(Integer, ForeignKey("user.username"))
    created_at = Column(DateTime, default=datetime.utcnow)
    action = Column(String)
    state = Column(String)

    user = relationship("User", back_populates="commands")
