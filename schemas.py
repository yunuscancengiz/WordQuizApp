from pydantic import BaseModel, Field
from datetime import datetime

### routers/auth.py ###

class CreateUserRequest(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    role: str = Field(default='user')


class Token(BaseModel):
    access_token: str
    token_type: str


### routers/users.py ###

class UserVerification(BaseModel):
    password: str
    new_password: str = Field(min_length=6)


### routers/words.py ###

class CreateWordRequest(BaseModel):
    word: str = Field(min_length=1, max_length=50)
    translition: str = Field(min_length=1, max_length=50)
    example_sentence: str = Field(min_length=1, max_length=200)


class WordUpdateRequest(BaseModel):
    word: str = Field(min_length=1, max_length=50)
    meaning: str = Field(min_length=1, max_length=50)
    sentence: str = Field(min_length=1, max_length=200)


class CorrectIncorrectRequest(BaseModel):
    is_last_time_correct: bool = Field(default=False)


class SentenceRequest(BaseModel):
    sentence: str = Field(min_length=3, max_length=100)


### routers/flashcards.py ###

class AnswerRequest(BaseModel):
    user_answer: str = Field(min_length=1, max_length=50)
    current_word: str = Field(min_length=1, max_length=50)


### routers/ros.py ###

class SentenceAnswerRequest(BaseModel):
    user_answer: str = Field(min_length=1, max_length=200)
    current_sentence: str = Field(min_length=1, max_length=200)


# routers/themes.py

class CreateThemeRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    darkcolor: str = Field(min_length=7, max_length=7)
    midcolor: str = Field(min_length=7, max_length=7)
    lightcolor: str = Field(min_length=7, max_length=7)
    is_default: bool = Field(default=False)


class ThemeOut(BaseModel):
    id: int
    name: str
    darkcolor: str
    midcolor: str
    lightcolor: str
    is_default: bool
    is_favorite: bool = False
    is_active: bool

    class Config:
        from_attributes = True


# routers/songs.py

class CreateSongRequest(BaseModel):
    date: datetime = Field()
    song_name: str = Field(min_length=1, max_length=100)
    spotify_url: str = Field(min_length=10, max_length=100)


class SongOut(BaseModel):
    id: int
    date: str
    song_name: str
    spotify_url: str

    class Config:
        from_attributes = True
