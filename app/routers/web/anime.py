from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.anime import AnimeORM
from app.models.user import UserORM

templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/anime", tags=["web"])

@router.get("/{anime_id}", response_class=HTMLResponse)
def anime_detail(request: Request, anime_id: int, db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    anime = db.execute(select(AnimeORM).where(AnimeORM.id == anime_id)).scalar_one_or_none()

    if anime is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Ánime no encontrado")
    
    return templates.TemplateResponse(
        "detail/anime.html",
        {"request": request, "anime": anime, "user": user}
    )