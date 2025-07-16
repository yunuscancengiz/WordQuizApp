from fastapi import APIRouter, Request, Depends, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated
import os
import json
from collections import defaultdict
from pathlib import Path
from .auth import get_current_user, redirect_to_login


BASE_DIR = Path(__file__).resolve().parent.parent
router = APIRouter(prefix='/conjugations', tags=['conjugations'])
templates = Jinja2Templates(directory=str(BASE_DIR / 'templates'))
user_dependency = Annotated[dict, Depends(get_current_user)]

# JSON verisini yükle
json_path = os.path.join(os.path.dirname(__file__), '..', 'static', 'verbs.json')
with open(json_path, mode='r', encoding='utf-8') as f:
    try:
        verb_data = json.load(f)
    except json.JSONDecodeError:
        verb_data = {"verbs": {}}


@router.get('/', response_class=HTMLResponse)
async def show_search_page(request: Request):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))
        if user is None:
            redirect_to_login()
        else:
            return templates.TemplateResponse('conjugation.html', {'request': request})
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
