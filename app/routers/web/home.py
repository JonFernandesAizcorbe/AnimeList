"""
Ruta web para pagina de inicio
Renderiza un HTML
"""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func, select

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.anime import AnimeORM
from app.models.anime_list import AnimeListORM
from app.models.genre import GenreORM
from app.models.user import UserORM

# configrar jinja2
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = None, g: str | None = None , db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()
    animes_top = db.execute(select(AnimeORM, func.count(AnimeListORM.user_id)).join(AnimeListORM).where(AnimeListORM.status == "Viendo").group_by(AnimeORM.id).order_by(func.count(AnimeListORM.user_id).desc()).limit(20)).scalars().all()
    scores = db.execute(select(AnimeORM, func.avg(AnimeListORM.score).label("avg_score")).join(AnimeListORM, AnimeListORM.anime_id == AnimeORM.id).group_by(AnimeORM.id).order_by(func.avg(AnimeListORM.score).desc())).all()
    
    result = None

    if q and q.strip():
        result = db.execute(select(AnimeORM).where(AnimeORM.name.ilike(f"%{q.strip()}%"))).scalars().all()

    result_g = None
    g_value = None
    
    if g and g.strip():
        try:
            g_value = int(g.strip())
            result_g = db.execute(select(AnimeORM).join(AnimeORM.genres).where(GenreORM.id == g_value)).scalars().all()
        
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
    next: str = Form(...),
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):

    entry = db.execute(select(AnimeListORM).where(AnimeListORM.anime_id == anime_id, AnimeListORM.user_id == user.id)).scalar_one_or_none()

    if entry and entry.status == "Inactivo":
        entry.status="Viendo"
        db.commit()
        db.refresh(entry)
    elif entry and entry.status != "Inactivo":
        entry.status="Inactivo"
        db.commit()
        db.refresh(entry)
    else:
        new_entry = AnimeListORM(user_id=user.id, anime_id=anime_id)
        db.add(new_entry)
        db.commit()
        db.refresh(new_entry)


    return RedirectResponse(next, status_code=303)
    
        


                
    

    




