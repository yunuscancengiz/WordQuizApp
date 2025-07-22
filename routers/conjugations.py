from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from collections import defaultdict
import traceback
from utils.auth_utils import redirect_to_login, get_current_user
from config import templates
from utils.conjugation_utils import load_json_data
from dependencies import db_dependency
from models import Users, Themes


router = APIRouter(prefix='/conjugations', tags=['conjugations'])


verb_data = load_json_data()    # load conjugations data from /static/verbs.json


@router.get('/', response_class=HTMLResponse)
async def show_search_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()
        return templates.TemplateResponse('conjugation.html', {'request': request, 'user': user, 'theme': theme_model})
    except:
        print(traceback.format_exc())
        return redirect_to_login()


@router.get('/{verb}', response_class=HTMLResponse)
async def show_conjugation(request: Request, db: db_dependency, verb: str):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()
        
        verb = verb.lower()
        data = verb_data.get('verbs', {}).get(verb)

        if not data:
            return templates.TemplateResponse('conjugation_table.html', {
                'request': request,
                'user': user,
                'theme': theme_model,
                'verb': verb,
                'info': [],
                'conjugations': [],
                'not_found': True
            })

        info = data.get('info', [])
        conjugations_raw = data.get('conjugations', [])

        # conjugations'ı mode-temporal olarak grupla
        grouped = defaultdict(list)
        for item in conjugations_raw:
            grouped[item.get("mode", "Unknown")].append({
                "tense": item.get("tense", "Unknown"),
                "entries": item.get("entries", [])
            })

        structured_conjugations = [{"mode": mode, "tenses": tenses} for mode, tenses in grouped.items()]

        return templates.TemplateResponse('conjugation_table.html', {
            'request': request,
            'user': user,
            'theme': theme_model,
            'verb': data.get("verb", verb),
            'info': info,
            'conjugations': structured_conjugations,
            'not_found': False
        })
    except:
        redirect_to_login()
