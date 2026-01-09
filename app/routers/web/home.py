"""
Ruta web para pagina de inicio
Renderiza un HTML
"""

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.database import get_db
from app.models.anime import AnimeORM
from app.models.genre import GenreORM

# configrar jinja2
templates = Jinja2Templates(directory="app/templates")

# crear router para rutas web de home
router = APIRouter(tags=["web"])

@router.get("/", response_class=HTMLResponse)
def home(request: Request, q: str | None = None, g: str | None = None , db: Session = Depends(get_db)):
    genres = db.execute(select(GenreORM).order_by(GenreORM.name.asc())).scalars().all()

    
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
        {"request": request, "genres": genres, "q": q, "result": result, "g": g, "g_value": g_value, "result_g": result_g}
    )