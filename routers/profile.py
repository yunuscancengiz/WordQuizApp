from fastapi import APIRouter, Request, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy import func
import traceback
from ..dependencies import db_dependency
from ..config import templates, bcrypt_context
from ..models import Users, CorrectIncorrect, Words, QuizStreaks, DailyStreaks, Themes
from ..utils.auth_utils import redirect_to_login, get_current_user
from ..schemas import UserVerification


router = APIRouter(prefix="/profile", tags=["profile"])


@router.get("/", response_class=HTMLResponse)
async def profile_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get("access_token"))

        # Kullanıcı modeli
        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()

        # Temel bilgiler
        full_name = f"{user_model.first_name} {user_model.last_name}"
        username = user_model.username
        email = user_model.email

        # İstatistikler
        correct_data = db.query(
            func.sum(CorrectIncorrect.correct_count),
            func.sum(CorrectIncorrect.incorrect_count)
        ).filter(CorrectIncorrect.owner_id == user.get("id")).first()

        correct_count = correct_data[0] or 0
        incorrect_count = correct_data[1] or 0
        total_questions = correct_count + incorrect_count

        all_time_max_streak = db.query(
            func.max(DailyStreaks.max_streak)
        ).filter(
            QuizStreaks.owner_id == user.get("id")
        ).scalar() or 0

        total_words = db.query(Words).filter(Words.owner_id == user.get("id")).count()

        # Active Days
        active_days = db.query(DailyStreaks.date).filter(
            DailyStreaks.owner_id == user.get("id")
        ).distinct().count()

        active_days = 53    # @TODO: delete later
        # Badge belirleme
        badges = []
        if active_days >= 10:
            badges.append("badges/10days-badge.png")
        if active_days >= 30:
            badges.append("badges/30days-badge.png")
        if active_days >= 50:
            badges.append("badges/50days-badge.png")

        # About (şimdilik dummy - gelecekte Users tablosuna about alanı eklenebilir)
        about = f"Hi! I'm {full_name}, and I'm on a mission to master French!"

        return templates.TemplateResponse("profile.html", {
            "request": request,
            "theme": theme_model,
            "user": {
                "sub": username,
                "full_name": full_name,
                "username": username,
                "email": email,
                "about": about
            },
            "total_questions": total_questions,
            "correct_count": correct_count,
            "incorrect_count": incorrect_count,
            "all_time_max_streak": all_time_max_streak,
            "total_words": total_words,
            "active_days": active_days,
            "badges": badges
        })

    except Exception:
        print(traceback.format_exc())
        return redirect_to_login()
    

