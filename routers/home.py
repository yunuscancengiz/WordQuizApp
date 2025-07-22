from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from starlette.responses import RedirectResponse
from pathlib import Path
from datetime import datetime, timedelta
import traceback
from ..config import templates
from ..models import QuizStreaks, Users, Songs, CorrectIncorrect, Words
from ..dependencies import db_dependency
from ..utils.auth_utils import redirect_to_login, get_current_user
from ..utils.theme_utils import get_theme_by_id


router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        streak = max_streak = 0
        streak_model = db.query(QuizStreaks).filter(QuizStreaks.owner_id == user.get("id")).first()
        if streak_model:
            streak = streak_model.streak
            max_streak = streak_model.max_streak

        theme_id = db.query(Users.theme_id).filter(Users.id == user.get("id")).scalar()
        theme = get_theme_by_id(db=db, theme_id=theme_id)
        
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        song = db.query(Songs).filter(Songs.date == today).first()
        if not song:
            song = db.query(Songs).filter(Songs.id == 1).first()


        tomorrow = today + timedelta(days=1)
        today_count = db.query(CorrectIncorrect).filter(
            CorrectIncorrect.owner_id == user.get("id"),
            CorrectIncorrect.last_attempted_at >= today,
            CorrectIncorrect.last_attempted_at < tomorrow
        ).count()

        word_count = db.query(Words).filter(Words.owner_id == user.get("id")).count()

        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "user": user,
                "streak": streak,
                "max_streak": max_streak,
                "today_question_count": today_count,
                "total_words": word_count,
                "theme": theme,
                "song": song
            },
        )
    except Exception as e:
        print(traceback.format_exc())
        return redirect_to_login()
    