"""
Router de páginas web
Contiene los endpoints que renderizan HTMLs
"""
from app.routers.web import anime, auth, character, home, actor
from app.routers.web import user
from fastapi import APIRouter


router = APIRouter()

router.include_router(home.router)
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(anime.router)
router.include_router(character.router)
router.include_router(actor.router)

__all__ = ["home", "auth", "user", "anime", "character", "actor"]