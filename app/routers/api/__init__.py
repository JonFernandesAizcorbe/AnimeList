"""
Routers de API REST
Contiene los endpoints que devuelven datos en JSON
"""

from fastapi import APIRouter
from app.routers.api import users

#router principal
router = APIRouter()

# incluir router de users en router principal
router.include_router(users.router)