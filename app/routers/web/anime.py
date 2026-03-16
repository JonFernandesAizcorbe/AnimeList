from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.anime import AnimeORM
from app.models.anime_list import AnimeListORM, display_status
from app.models.user import UserORM


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/anime", tags=["web"])

@router.get("/{anime_id}", response_class=HTMLResponse)
def anime_detail(request: Request, anime_id: int, db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):

    since_30 = datetime.now() - timedelta(days=30)
    anime = db.execute(select(AnimeORM).where(AnimeORM.id == anime_id)).scalar_one_or_none()
    score_list = db.execute(select(AnimeORM, func.round(func.avg(AnimeListORM.score)).label("avg_score")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).where(AnimeListORM.score.is_not(None)).group_by(AnimeORM.id).order_by(func.avg(AnimeListORM.score).desc())).all()
    like_list = db.execute(select(AnimeORM, func.count(AnimeListORM.user_id).label("likes")).outerjoin(AnimeListORM, and_(AnimeListORM.anime_id == AnimeORM.id, AnimeListORM.like.is_(True), AnimeListORM.date_like >= since_30)).group_by(AnimeORM.id).order_by(func.count(AnimeListORM.user_id).desc())).all()

    status_options = display_status.enums

    rank_like = None
    for i , (a, likes) in enumerate(like_list, start=1):
        if a.id == anime_id:
            rank_like = i
            break

    rank = None
    for i, (a, svg_score) in enumerate(score_list, start=1):
        if a.id == anime_id:
            rank = i
            break


    my_list = None
    in_list = None

    if user is not None:
        my_list = db.execute(select(AnimeListORM).where(and_(AnimeListORM.user_id == user.id, AnimeListORM.anime_id == anime_id))).scalar_one_or_none()
        in_list = db.execute(select(AnimeListORM).where(AnimeListORM.anime_id == anime.id, AnimeListORM.user_id == user.id)).scalar_one_or_none()

    if anime is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - Ánime no encontrado")
    
    return templates.TemplateResponse(
        "detail/anime.html",
        {"request": request, "anime": anime, "user": user, "my_list": my_list, "rank": rank, "rank_like": rank_like, "status_options": status_options, "in_list": in_list}
    )


@router.post("/delete", response_class=HTMLResponse)
def status_delete(
    request: Request,
    anime_id: int = Form(...),
    next: str = Form(...),
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):
    
    anime = db.execute(select(AnimeListORM).where(AnimeListORM.anime_id == anime_id, AnimeListORM.user_id == user.id)).scalar_one_or_none()

    if anime:
        anime.status = "Eliminado"
        db.commit()
        db.refresh(anime)

        return RedirectResponse(next, status_code=303)
