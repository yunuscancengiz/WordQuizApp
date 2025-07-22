from fastapi import APIRouter, Request, status, HTTPException, Path
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy import or_, and_
from typing import List
import traceback
from models import Songs
from schemas import CreateSongRequest, SongOut
from dependencies import db_dependency
from config import templates
from utils.auth_utils import redirect_to_login, get_current_user


router = APIRouter(prefix='/songs', tags=['songs'])


### Pages ###


### Endpoints ###

@router.get('/all', response_model=List[SongOut])
async def list_all_songs(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    response = []
    all_songs = db.query(Songs).all()
    for song in all_songs:
        response.append(
            SongOut(
                id=song.id,
                date=song.date,
                song_name=song.song_name,
                spotify_url=song.spotify_url
            )
        )
    return response


@router.post('/create')
async def create_song(request: Request, db: db_dependency, create_song_request: CreateSongRequest):
    user = await get_current_user(token=request.cookies.get('access_token'))

    date = create_song_request.date
    song_name = create_song_request.song_name
    spotify_url = create_song_request.spotify_url

    if not all([date, song_name, spotify_url]):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='All fields are required!')
    
    existing = db.query(Songs).filter(
        or_(
            Songs.date.ilike(date),
            Songs.song_name.ilike(song_name),
            Songs.spotify_url.ilike(spotify_url)
        )
    ).first()

    if existing:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={'message': 'Song already exists!'}
        )
    
    song_model = Songs(
        date=date,
        song_name=song_name,
        spotify_url=spotify_url
    )
    db.add(song_model)
    db.commit()
    db.refresh(song_model)

    return {
        'message': 'Song created successfully!',
        'song_id': song_model.id
    }


@router.post('/bulk-create')
async def bulk_create_songs(request: Request, db: db_dependency, song_list: List[CreateSongRequest]):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Only admins can bulk create themes.')

    created = []
    skipped = []

    for song_data in song_list:
        existing = db.query(Songs).filter(
            or_(
                Songs.date.ilike(song_data.date),
                Songs.song_name.ilike(song_data.song_name),
                Songs.spotify_url.ilike(song_data.spotify_url)
            )
        ).first()

        if existing:
            skipped.append(song_data.song_name)
            continue

        new_song = Songs(
            date=song_data.date,
            song_name=song_data.song_name,
            spotify_url=song_data.spotify_url
        )
        db.add(new_song)
        created.append(song_data.song_name)
    db.commit()

    return {
        'message': 'Songs processed.',
        'created': created,
        'skipped': skipped
    }


@router.delete('/delete-all')
async def delete_all_songs(request: Request, db: db_dependency):
    user = await get_current_user(token=request.cookies.get('access_token'))

    if user['user_role'] != 'admin':
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Only admins can delete all songs.'
        )

    deleted_count = db.query(Songs).delete()
    db.commit()

    return {
        'message': f'{deleted_count} songs deleted successfully.'
    }


@router.delete('/{song_id}')
async def delete_song(request: Request, db: db_dependency, song_id: int = Path(gt=0)):
    user = await get_current_user(token=request.cookies.get('access_token'))

    song = db.query(Songs).filter(Songs.id == song_id).first()
    if not song:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Song not found!')
    
    db.delete(song)
    db.commit()
    return {'message': f'Song "{song.song_name}" deleted successfully.'}



