# AnimeList — Descripción del proyecto

## Resumen
AnimeList es una aplicación web en FastAPI para mantener un catálogo de animes y permitir a los usuarios crear listas personales donde registrar qué han visto, su estado (viendo, completado, dropeado, "lo veré"), puntuaciones y comentarios.

## Características principales
- Registro y autenticación de usuarios.
- Catálogo de animes con detalle (imagen, descripción, estudio, capítulos, géneros, personajes, actores de doblaje).
- Listas personales por usuario (añadir/editar/eliminar entradas, puntuación, fechas, estado).
- Rutas web (plantillas Jinja2) y API REST para operaciones sobre animes.
- Middleware de sesiones para manejo de sesión vía cookies.
- Carpeta `app/static` para recursos estáticos (CSS, JS, imágenes) y `app/templates` para vistas.

## Estructura principal del proyecto
- `main.py` — arranca la aplicación con Uvicorn.
- `app/main.py` — instancia la app FastAPI, monta `static`, añade `SessionMiddleware`, inicializa la BD y registra routers.
- `app/database.py` — inicialización y helpers de la base de datos (se invoca `init_db()` al arrancar).
- `app/routers/` — contiene los routers organizados en `api/` y `web/`:
  - `app/routers/api/` — endpoints JSON (p. ej. `prefix="/api/animes"`).
  - `app/routers/web/` — vistas con plantillas y formularios (p. ej. `prefix="/anime"`).
- `app/models/` — modelos ORM (SQLAlchemy) como `AnimeORM`, `UserORM`, `GenreORM`, `AnimeListORM`, tablas intermedias.
- `app/schemas/` — modelos Pydantic para validación y serialización (create/patch/response).
- `app/auth/` — dependencias y validadores para autenticación y autorización.
- `app/templates/` — plantillas Jinja2 (`home.html`, `detail/anime.html`, `login/register`, etc.).
- `app/static/` — estilos, imágenes y scripts.

## Modelos relevantes (visión rápida)
- `UserORM` — usuarios con email, hash de contraseña, perfil, imagen y created_at.
- `AnimeORM` — animes con nombre, descripción, capítulos, imagen, banner, color, relaciones con géneros, personajes y listas de usuarios.
- `AnimeListORM` — tabla intermedia usuario↔anime para estado, puntuación, comentarios, fechas.
- Tablas intermedias para relaciones many-to-many (actores, géneros, amigos, etc.).

## Rutas y vistas importantes
- Web:
  - `/` — inicio (lista/filtrado de animes).
  - `/anime/{anime_id}` — detalle de un anime (plantilla `detail/anime.html`).
  - Formularios POST para añadir/eliminar o cambiar estado en la lista.
- API (JSON):
  - `/api/animes` — endpoints REST para listar/crear/actualizar animes (implementación parcial en `app/routers/api/animes.py`).

## Tecnologías y dependencias
Revisar `requirements.txt`, entre ellas: `fastapi`, `uvicorn`, `SQLAlchemy`, `pydantic`, `Jinja2`, `python-multipart`, `passlib`.

## Cómo ejecutar (desarrollo)
Usualmente se lanza con Uvicorn. Desde la raíz del proyecto:

```bash
python main.py
# o directamente
uvicorn app.main:app --reload
```