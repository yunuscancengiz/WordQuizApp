from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime,  Date
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime, timezone
from zoneinfo import ZoneInfo


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
    theme_id = Column(Integer, ForeignKey("themes.id"), nullable=True, default=1)


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
    correct_count = Column(Integer, default=0)
    incorrect_count = Column(Integer, default=0)
    last_attempted_at = Column(DateTime, default=lambda: datetime.now(tz=ZoneInfo('Europe/Istanbul')))
    created_at = Column(DateTime, default=lambda: datetime.now(tz=ZoneInfo('Europe/Istanbul')))
    owner_id = Column(Integer, ForeignKey('users.id'))
    word_id = Column(Integer, ForeignKey('words.id'))


class DailyStreaks(Base):
    __tablename__ = 'daily_streaks'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, default=datetime.now())
    max_streak = Column(Integer)
    question_count = Column(Integer, default=0)
    owner_id = Column(Integer, ForeignKey('users.id'))


class QuizStreaks(Base):
    __tablename__ = 'quiz_streaks'

    id = Column(Integer, primary_key=True, index=True)
    streak = Column(Integer, default=0)
    max_streak = Column(Integer, default=0)
    question_count = Column(Integer, default=0)
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
    mode = Column(String)
    tense = Column(String)                           # imparfait
    verb = Column(String, index=True)                # agir
    person = Column(String)                          # je
    stem = Column(String)                            # agiss
    ending = Column(String)                          # ais
    full_form = Column(String)                       # j'agissais


class Themes(Base):
    __tablename__ = "themes"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    darkcolor = Column(String, nullable=False)
    midcolor = Column(String, nullable=False)
    lightcolor = Column(String, nullable=False)
    is_default = Column(Boolean, default=False)


class UserThemeFavorite(Base):
    __tablename__ = "user_theme_favorites"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    theme_id = Column(Integer, ForeignKey("themes.id"))

    __table_args__ = (UniqueConstraint("user_id", "theme_id", name="_user_theme_uc"),)

