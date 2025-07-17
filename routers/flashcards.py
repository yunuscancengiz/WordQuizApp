from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from pydantic import BaseModel, Field
from pathlib import Path
import random
from .auth import get_current_user, get_db, redirect_to_login
from ..models import Words, Sentences


BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter(prefix='/flashcards', tags=['flashcards'])
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


### Pages ###

@router.get('/', response_class=HTMLResponse)
async def show_search_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            redirect_to_login()

        words = db.query(Words).filter(Words.owner_id == user.get('id')).all()
        if words:
            random.shuffle(words)
        word = words[0]
        sentences = db.query(Sentences.sentence).filter(Sentences.word_id == word.id).all()
        sentences = [sentence[0] for sentence in sentences]
        print(sentences)
        return templates.TemplateResponse('flashcards.html', {'request': request, 'word': word.word, 'sentences': sentences})
    except:
        redirect_to_login()



### Endpoints ###

