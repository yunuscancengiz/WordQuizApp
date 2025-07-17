from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from collections import defaultdict
from ..utils.auth_utils import get_current_user, redirect_to_login
from ..config import templates
from ..utils.conjugation_utils import load_json_data


router = APIRouter(prefix='/conjugations', tags=['conjugations'])


verb_data = load_json_data()    # load conjugations data from /static/verbs.json


@router.get('/', response_class=HTMLResponse)
async def show_search_page(request: Request):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            redirect_to_login()
        else:
            return templates.TemplateResponse('conjugation.html', {'request': request, 'user': user})
    except:
        redirect_to_login()


@router.get('/{verb}', response_class=HTMLResponse)
async def show_conjugation(request: Request, verb: str):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            return redirect_to_login()
        
        verb = verb.lower()
        data = verb_data.get('verbs', {}).get(verb)

        if not data:
            return templates.TemplateResponse('conjugation_table.html', {
                'request': request,
                'user': user,
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
            'verb': data.get("verb", verb),
            'info': info,
            'conjugations': structured_conjugations,
            'not_found': False
        })
    except:
        redirect_to_login()
