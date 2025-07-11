from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from .auth import get_current_user
from typing import Annotated

router = APIRouter()
templates = Jinja2Templates(directory='WordQuizApp/templates')

user_dependency = Annotated[dict, Depends(get_current_user)]
user = {'sub': 'username', 'id': 'user_id', 'user_role': 'user_role'}

@router.get("/", response_class=HTMLResponse)
async def home(request: Request, user=user):
    return templates.TemplateResponse("index.html", {"request": request, "user": user})
