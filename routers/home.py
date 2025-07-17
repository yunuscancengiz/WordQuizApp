from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from pathlib import Path
from ..utils.auth_utils import get_current_user
from ..config import templates
from ..models import QuizStreaks
from ..dependencies import db_dependency
from ..utils.auth_utils import redirect_to_login


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: db_dependency):
    #token = request.cookies.get("access_token")
    #if not token:
    #    return RedirectResponse(url='/auth/login-page', status_code=302)

    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()

        streak = max_streak = 0
        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get('id')).first()
        if streak_model:
            streak = streak_model.streak
            max_streak = streak_model.max_streak
        return templates.TemplateResponse("home.html", {"request": request, "user": user, 'streak': streak, 'max_streak': max_streak})
    except Exception as e:
        return redirect_to_login()

    