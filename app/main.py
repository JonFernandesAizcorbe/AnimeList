from fastapi import  FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware

from app.database import init_db
from app.routers.api import router as api_router
from app.routers.web import router as web_router
"""
Configuración de la aplicación FastAPI
"""


# crea la instancia de la aplicación FastAPI
app = FastAPI(title="AnimeList", version="1.0.0")


# 🔐 Middleware de sesiones (COOKIE)
app.add_middleware(
    SessionMiddleware,
    secret_key="8P7yXzYDd2bVw_evilCelzKChuOiYsOlRKL2NRsF-zIQl2EEKVsPASjtqb7mMUtF5KiANn9JSquxBDnWRcA2vw",
    session_cookie="session_id",
    max_age=60 * 60,     # 1 hora
    same_site="lax",
    https_only=False    # True en producción
)

# Montar la carpeta static
app.mount("/static", StaticFiles(directory="app/static/"), name="static")

# inicializa la base de datos con animes por defecto
init_db()



# registrar los routers
app.include_router(api_router)
app.include_router(web_router)


