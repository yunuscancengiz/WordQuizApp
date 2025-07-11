from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from .models import Base
from .database import engine
from .routers import auth, words, admin, users, conjugations, index



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.mount('/static', StaticFiles(directory='WordQuizApp/static'), name='static')

### Endpoints ###




### Routers ###
app.include_router(router=auth.router)
app.include_router(router=admin.router)
app.include_router(router=users.router)
app.include_router(router=words.router)
app.include_router(router=conjugations.router)
app.include_router(router=index.router)