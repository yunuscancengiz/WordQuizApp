from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date
from datetime import datetime
from sqlalchemy.schema import UniqueConstraint


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


class Sentences(Base):
    __tablename__ = 'sentences'

    id = Column(Integer, primary_key=True, index=True)
    sentence = Column(String)
    word_id = Column(Integer, ForeignKey('words.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))


class CorrectIncorrect(Base):
    __tablename__ = 'correct_incorrect'
    __table_args__ = (UniqueConstraint('owner_id', 'word_id', name='_owner_word_uc'),)

    id = Column(Integer, primary_key=True, index=True)
    is_last_time_correct = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))


class DailyStreaks(Base):
    __tablename__ = 'daily_streaks'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now())
    max_streak = Column(Integer)
    owner_id = Column(Integer, ForeignKey('users.id'))


class QuizStreaks(Base):
    __tablename__ = 'quiz_streaks'

    id = Column(Integer, primary_key=True, index=True)
    streak = Column(Integer, default=0)
    max_streak_id = Column(Integer, ForeignKey('daily_streaks.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))


class Songs(Base):
    __tablename__ = 'songs'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True)
    song_name = Column(String)
    spotify_url = Column(String)


class Conjugations(Base):
    __tablename__ = 'conjugations'

    id = Column(Integer, primary_key=True, index=True)
    verb = Column(String, index=True)                # agir
    stem = Column(String)                            # agiss
    ending = Column(String)                          # ais
    full_form = Column(String)                       # j'agissais
    person = Column(String)                          # je
    tense = Column(String)                           # imparfait