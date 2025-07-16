from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user, get_db, redirect_to_login
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter(prefix='/flashcards', tags=['flashcards'])
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get('/', response_class=HTMLResponse)
async def show_search_page(request: Request):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            redirect_to_login()
        else:
            return templates.TemplateResponse('flashcards.html', {'request': request})
    except:
        redirect_to_login()