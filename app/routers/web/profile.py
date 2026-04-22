
from datetime import datetime

from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.anime import AnimeORM
from app.models.anime_list import AnimeListORM
from app.models.user import UserORM
from app.auth import user_require


router = APIRouter(prefix="/profile", tags=["profile"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def user_required(request: Request, db: Session = Depends(get_db), user: UserORM = Depends(user_require)):
    date = datetime.now()
    anime = db.execute(select(AnimeORM)).scalars().first()
    last_animes = db.execute(select(AnimeListORM).where(AnimeListORM.user_id == user.id, AnimeListORM.status != "Eliminado").order_by(AnimeListORM.date_like.asc()).limit(5)).scalars().all()
    activity = db.execute(select(AnimeListORM).where(AnimeListORM.user_id == user.id, AnimeListORM.date_like < date).order_by(AnimeListORM.date_like.desc()).limit(4)).scalars().all()

    hours = []

    for a in activity:
        time = (date - a.date_like).total_seconds() / 3600 # convert to hours
        hours.append(time)


    return templates.TemplateResponse(
        "profile/profile.html",
        {"request": request, "user": user, "anime": anime, "activity": activity, "hours": hours, "last_animes": last_animes}
    )

        

@router.get("/list", response_class=HTMLResponse)
def list_anime(request: Request, db: Session = Depends(get_db), user: UserORM = Depends(user_require)):

    anime_finish = db.execute(select(AnimeListORM).where(AnimeListORM.user_id == user.id, AnimeListORM.status == "Completado")).scalars().all()
    anime_view = db.execute(select(AnimeListORM).where(AnimeListORM.user_id == user.id,AnimeListORM.status == "Viendo")).scalars().all()
    
    return templates.TemplateResponse(
        "profile/list.html",
        {"request": request, "user": user, "anime_finish": anime_finish, "anime_view": anime_view}
    )