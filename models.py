from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)


class Words(Base):
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
    meaning = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))


class Streaks(Base):
    __tablename__ = 'streaks'

    id = Column(Integer, primary_key=True, index=True)
    streak_count = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))


class CorrectIncorrect(Base):
    __tablename__ = 'correct_incorrect'

    id = Column(Integer, primary_key=True, index=True)
    is_last_time_correct = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))