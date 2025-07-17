from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .database import engine, Base
from .routers import auth, words, admin, users, conjugations, home, flashcards, ros, quiz



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='OuiCherie/static'), name='static')

### Endpoints ###




### Routers ###
app.include_router(router=auth.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)
app.include_router(router=words.router)
app.include_router(router=conjugations.router)
app.include_router(router=home.router)
app.include_router(router=flashcards.router)
app.include_router(router=ros.router)
app.include_router(router=quiz.router)