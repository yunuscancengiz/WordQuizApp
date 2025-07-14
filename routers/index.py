from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from .auth import get_current_user, get_db, JWTError
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent



router = APIRouter()
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))

db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url='/auth/login-page', status_code=302)

    try:
        user = await get_current_user(token=token)
    except Exception as e:
        print("Auth error:", e)
        return RedirectResponse(url='/auth/login-page', status_code=302)

    return templates.TemplateResponse("index.html", {"request": request, "user": user})