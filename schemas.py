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

class WordRequest(BaseModel):
    word: str = Field(min_length=1, max_length=100)
    meaning: str = Field(min_length=1, max_length=100)


class CorrectIncorrectRequest(BaseModel):
    is_last_time_correct: bool = Field(default=False)


class SentenceRequest(BaseModel):
    sentence: str = Field(min_length=3, max_length=100)


### routers/flashcards.py ###

class AnswerRequest(BaseModel):
    user_answer: str = Field(min_length=1, max_length=50)
    current_word: str = Field(min_length=1, max_length=50)