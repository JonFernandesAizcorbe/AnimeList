"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from fastapi import APIRouter
from app.routers.api import songs

#router principal
router = APIRouter()

# incluir router de sons en router principal
router.include_router(songs.router)