from fastapi import  FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router
"""
Configuración de la aplicación FastAPI
"""


# crea la instancia de la aplicación FastAPI
app = FastAPI(title="Cancioncitas", version="1.0.0")

# Montar la carpeta static
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# inicializa la base de datos con canciones por defecto
init_db()



# registrar los routers
app.include_router(api_router)
app.include_router(web_router)


