from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from pathlib import Path
from .auth import get_current_user
from ..dependencies import templates


router = APIRouter()


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