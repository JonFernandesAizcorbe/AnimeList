
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.anime import AnimeORM
from app.models.user import UserORM
from app.auth import user_require


router = APIRouter(prefix="/profile", tags=["profile"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
def user_required(request: Request, db: Session = Depends(get_db), user: UserORM = Depends(user_require)):
    anime = db.execute(select(AnimeORM)).scalars().first()
    return templates.TemplateResponse(
        "profile/profile.html",
        {"request": request, "user": user, "anime": anime}
    )
        