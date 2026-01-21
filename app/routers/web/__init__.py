"""
Router de páginas web
Contiene los endpoints que renderizan HTMLs
"""
from app.routers.web import auth, home
from app.routers.web import user
from fastapi import APIRouter


router = APIRouter()

router.include_router(home.router)
router.include_router(auth.router)
router.include_router(user.router)

__all__ = ["home", "auth", "user"]