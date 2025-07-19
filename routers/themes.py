from fastapi import APIRouter, Path, Request, HTTPException, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import or_, and_
from typing import List
import traceback
from ..models import Themes, UserThemeFavorite, Users
from ..schemas import CreateThemeRequest, ThemeOut
from ..dependencies import db_dependency
from ..config import templates
from ..utils.auth_utils import redirect_to_login, get_current_user
from ..utils.db_utils import set_default_theme


router = APIRouter(prefix='/themes', tags=['themes'])


### Pages ###

@router.get('/', response_class=HTMLResponse)
async def themes_page(request: Request, db: db_dependency):
    try:
        user = await get_current_user(token=request.cookies.get('access_token'))

        user_model = db.query(Users).filter(Users.id == user.get("id")).first()
        theme_model = db.query(Themes).filter(Themes.id == user_model.theme_id).first()

        all_themes = db.query(Themes).all()
        favorite_ids = {
            fav.theme_id
            for fav in db.query(UserThemeFavorite).filter(UserThemeFavorite.user_id == user.get('id')).all()
        }

        themes = []
        for theme in all_themes:
            themes.append(
                ThemeOut(
                    id=theme.id,
                    name=theme.name,
                    darkcolor=theme.darkcolor,
                    midcolor=theme.midcolor,
                    lightcolor=theme.lightcolor,
                    is_default=theme.is_default,
                    is_favorite=theme.id in favorite_ids,
                    is_active=theme.id == user_model.theme_id
                )
            )

        return templates.TemplateResponse(
            'themes.html',
            {'request': request, 'user': user, 'themes': themes, 'theme': theme_model}
        )

    except Exception as e:
        print(traceback.format_exc())
        return redirect_to_login()




### Endpoints ###

@router.get('/all', response_model=List[ThemeOut])
async def list_all_themes(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    all_themes = db.query(Themes).all()
    favorite_ids = {
        fav.theme_id
        for fav in db.query(UserThemeFavorite).filter(UserThemeFavorite.user_id == user.get('id')).all()
    }

    theme_id = db.query(Users.theme_id).filter(Users.id == user.get("id")).first()

    response = []
    for theme in all_themes:
        response.append(
            ThemeOut(
                id=theme.id,
                name=theme.name,
                darkcolor=theme.darkcolor,
                midcolor=theme.midcolor,
                lightcolor=theme.lightcolor,
                is_default=theme.is_default,
                is_favorite=theme.id in favorite_ids,
                is_active=theme.id == theme_id
            )
        )
    return response


@router.get('/favorites', response_model=List[ThemeOut])
async def list_favorite_themes(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    favorite_ids = {
        fav.theme_id
        for fav in db.query(UserThemeFavorite).filter(UserThemeFavorite.user_id == user.get('id')).all()
    }

    theme_id = db.query(Users.theme_id).filter(Users.id == user.get("id")).first()

    themes = db.query(Themes).filter(Themes.id.in_(favorite_ids)).all()

    response = []
    for theme in themes:
        response.append(
            ThemeOut(
                id=theme.id,
                name=theme.name,
                darkcolor=theme.darkcolor,
                midcolor=theme.midcolor,
                lightcolor=theme.lightcolor,
                is_default=theme.is_default,
                is_favorite=True,
                is_active=theme.id == theme_id
            )
        )
    return response



@router.post('/create')
async def create_theme(request: Request, db: db_dependency, create_theme_request: CreateThemeRequest):
    user = await get_current_user(token=request.cookies.get('access_token'))
    if user['user_role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authorized! Only admins can add theme.')
    
    name = create_theme_request.name
    darkcolor = create_theme_request.darkcolor
    midcolor = create_theme_request.midcolor
    lightcolor = create_theme_request.lightcolor
    is_default = create_theme_request.is_default

    if not all([name, darkcolor, midcolor, lightcolor]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='All fields are requeired!')
    
    existing = db.query(Themes).filter(
        or_(
            Themes.name.ilike(name),
            and_(
                Themes.darkcolor == darkcolor,
                Themes.midcolor == midcolor,
                Themes.lightcolor == lightcolor
            )
        )
    ).first()

    if existing:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Theme already exist!'}
        )
    
    if is_default:
        db.query(Themes).update({Themes.is_default: False})
    
    theme_model = Themes(
        name=name,
        darkcolor=darkcolor,
        midcolor=midcolor,
        lightcolor=lightcolor,
        is_default=is_default
    )
    db.add(theme_model)
    db.commit()
    db.refresh(theme_model)

    return {
        'message': 'Theme created successfully!',
        'theme_id': theme_model.id
    }


@router.post('/bulk-create')
async def bulk_create_themes(request: Request, db: db_dependency, theme_list: List[CreateThemeRequest]):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can bulk create themes.')

    created = []
    skipped = []

    for theme_data in theme_list:
        existing = db.query(Themes).filter(
            or_(
                Themes.name.ilike(theme_data.name),
                and_(
                    Themes.darkcolor == theme_data.darkcolor,
                    Themes.midcolor == theme_data.midcolor,
                    Themes.lightcolor == theme_data.lightcolor
                )
            )
        ).first()

        if existing:
            skipped.append(theme_data.name)
            continue

        if theme_data.is_default:
            db.query(Themes).update({Themes.is_default: False})

        new_theme = Themes(
            name=theme_data.name,
            darkcolor=theme_data.darkcolor,
            midcolor=theme_data.midcolor,
            lightcolor=theme_data.lightcolor,
            is_default=theme_data.is_default
        )

        db.add(new_theme)
        created.append(theme_data.name)

    db.commit()

    return {
        "message": "Themes processed.",
        "created": created,
        "skipped": skipped
    }


@router.post('/{theme_id}/favorite')
async def toggle_favorites(request: Request, db: db_dependency, theme_id: int = Path(ge=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    theme_exists = db.query(Themes).filter_by(id=theme_id).first()
    if not theme_exists:
        raise HTTPException(status_code=404, detail='Theme not found.')

    fav_theme_model = db.query(UserThemeFavorite).filter(
        UserThemeFavorite.user_id == user.get('id'),
        UserThemeFavorite.theme_id == theme_id
    ).first()

    if fav_theme_model:
        db.delete(fav_theme_model)
        db.commit()
        return {'message': 'Theme removed from favorites', 'is_favorite': False}
    else:
        new_fav_theme = UserThemeFavorite(
            user_id=user.get('id'),
            theme_id=theme_id,   
        )
        db.add(new_fav_theme)
        db.commit()
        db.refresh(new_fav_theme)
        return {'message': 'Theme added into favorites', 'is_favorite': True}
    

@router.patch('/use/{theme_id}')
async def use_theme(request: Request, db: db_dependency, theme_id: int = Path(ge=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    theme = db.query(Themes).filter_by(id=theme_id).first()
    if not theme:
        raise HTTPException(status_code=404, detail='Theme not found.')
    
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model:
        user_model.theme_id = theme_id
    db.commit()
    db.refresh(user_model)
    
    return {
        'message': f'Theme set to "{theme.name}" successfully.',
        'active_theme_id': user_model.theme_id,
        'theme': {
            'darkcolor': theme.darkcolor,
            'midcolor': theme.midcolor,
            'lightcolor': theme.lightcolor
        }
    }


@router.delete('/{theme_id}')
async def delete_theme(request: Request, db: db_dependency, theme_id: int = Path(ge=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can delete themes.')

    theme = db.query(Themes).filter_by(id=theme_id).first()
    if not theme:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Theme not found.')

    active_user_count = db.query(Themes).join(user.__class__).filter(user.__class__.theme_id == theme_id).count()
    if active_user_count > 0:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail='Theme is currently in use by one or more users.')

    db.query(UserThemeFavorite).filter_by(theme_id=theme_id).delete()
    db.delete(theme)
    db.commit()
    return {'message': f'Theme "{theme.name}" deleted successfully.'}
