"""
Ruta web para pagina de inicio
Renderiza un HTML
"""

from datetime import datetime

from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import Integer, and_, func, select

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.anime import AnimeORM
from app.models.anime_list import AnimeListORM, display_status
from app.models.genre import GenreORM
from app.models.user import UserORM

# configrar jinja2
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = None, g: str | None = None , db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()
    animes_top = db.execute(select(AnimeORM, func.sum(AnimeListORM.like.cast(Integer)).label("likes")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).where(AnimeListORM.like.is_(True)).group_by(AnimeORM.id).order_by(func.sum(AnimeListORM.like.cast(Integer)).desc()).limit(6)).all()
    scores = db.execute(select(AnimeORM, func.round(func.avg(AnimeListORM.score), 2).label("avg_score")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).group_by(AnimeORM.id).order_by(func.avg(AnimeListORM.score).desc())).all()

    result = None

    if q and q.strip():
        result = db.execute(select(AnimeORM).where(AnimeORM.name.ilike(f"%{q.strip()}%"))).scalars().all()

    result_g = None
    g_value = None
    
    if g and g.strip():
        try:
            g_value = int(g.strip())
            result_g = db.execute(select(AnimeORM).join(AnimeORM.genres).where(GenreORM.id == g_value).order_by(AnimeORM.name.asc())).scalars().all()
        
        except ValueError:
            pass

    
    return templates.TemplateResponse(
        "home.html",
        {"request": request, "genres": genres, "q": q, "result": result, "g": g, "g_value": g_value, "result_g": result_g, "user": user, "animes_top": animes_top, "scores": scores}
    )


@router.post("/addlist", response_class=HTMLResponse)
def add_list(
    request: Request,
    anime_id: int = Form(...),
    status: str = Form(...),
    score: str | None = Form(None),
    next: str = Form(...),
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):

    if user is None:
        return RedirectResponse(next, status_code=303)
    
    entry = db.execute(select(AnimeListORM).where(AnimeListORM.anime_id == anime_id, AnimeListORM.user_id == user.id)).scalar_one_or_none()

    enum_values = display_status.enums

    score = int(score) if score else None

    if status not in enum_values:
        status = "Viendo"

    if entry:
        entry.status = status
        entry.score = score

        db.commit()
        db.refresh(entry)

        return RedirectResponse(next, status_code=303)
    
    else:
        new_entry = AnimeListORM(
            anime_id=anime_id,
            user_id= user.id,
            status=status,
            score=score
        )

        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)

        return RedirectResponse(next, status_code=303)


    # if user is None:
    #     return RedirectResponse(next, status_code=303)

    # entry = db.execute(select(AnimeListORM).where(AnimeListORM.anime_id == anime_id, AnimeListORM.user_id == user.id)).scalar_one_or_none()

    # if entry and entry.status == "Eliminado":
    #     entry.status="Inactivo"
    #     db.commit()
    #     db.refresh(entry)
    # elif entry and entry.status != "Eliminado":
    #     entry.status="Eliminado"
    #     db.commit()
    #     db.refresh(entry)
    # else:
    #     new_entry = AnimeListORM(user_id=user.id, anime_id=anime_id, status="Inactivo")
    #     db.add(new_entry)
    #     db.commit()
    #     db.refresh(new_entry)


    # return RedirectResponse(url=next, status_code=303)


@router.post("/like", response_class=HTMLResponse)
def like(request: Request,
        anime_id: int = Form(...),
        next: str = Form(...),
        db: Session = Depends(get_db),
        user: UserORM = Depends(get_current_user)
):
    
    if user is None:
        return RedirectResponse(next, status_code=303)

    i_like = db.execute(select(AnimeListORM).where(and_(AnimeListORM.anime_id == anime_id, AnimeListORM.user_id == user.id))).scalar_one_or_none()

    if i_like and i_like.like == False:
        i_like.like = True
        i_like.date_like = datetime.now()
        db.commit()
        db.refresh(i_like)
    elif i_like and i_like.like == True:
        i_like.like = False
        i_like.date_like = None
        db.commit()
        db.refresh(i_like)
    else:
        new_list = AnimeListORM(anime_id=anime_id, user_id=user.id, like=True, date_like=datetime.now(), status="Eliminado")
        db.add(new_list)
        db.commit()
        db.refresh(new_list)

    response = RedirectResponse(url=next, status_code=303)
    response.headers["Cache-Control"] = "no-store"

    return response


@router.get("/popular", response_class=HTMLResponse)
def popular_list(request: Request, page: int = 1, db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    per_page = 12
    offset = (page - 1) * per_page

    popular = db.execute(select(AnimeORM, func.count(AnimeListORM.user_id)).join(AnimeListORM).where(AnimeListORM.like == True).group_by(AnimeORM.id).order_by(func.count(AnimeListORM.user_id).desc()).offset(offset).limit(per_page)).all()
    points = db.execute(select(AnimeORM, func.round(func.avg(AnimeListORM.score), 2).label("avg_score")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).group_by(AnimeORM.id).order_by(func.avg(AnimeListORM.score).desc())).all()
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()
    

    return templates.TemplateResponse(
        "filter/popular.html",
        {"request": request, "popular": popular, "page": page, "points": points, "user": user, "genres": genres}
    )

@router.get("/score", response_class=HTMLResponse)
def score_list(request: Request, page: int = 1, db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    per_page = 12
    offset = (page - 1) * per_page

    scores = db.execute(select(AnimeORM, func.round(func.avg(AnimeListORM.score),2).label("avg_score")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).group_by(AnimeORM.id).order_by(func.avg(AnimeListORM.score).desc()).offset(offset).limit(per_page)).all()
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()

    return templates.TemplateResponse(
        "filter/popular.html",
        {"request": request, "scores": scores, "page": page, "user": user, "genres": genres}
    )




                
    

    




