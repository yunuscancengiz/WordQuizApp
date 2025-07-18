from pydantic import BaseModel, Field


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

class WordUpdateRequest(BaseModel):
    word: str
    meaning: str
    sentence: str


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