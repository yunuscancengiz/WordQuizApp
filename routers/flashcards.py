from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user, get_db
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

router = APIRouter(prefix='/flashcards', tags=['flashcards'])
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
user = {'sub': 'username', 'id': 'user_id', 'user_role': 'user_role'}       # @TODO: going to be deleted



@router.get('', )
def get_word():
    pass