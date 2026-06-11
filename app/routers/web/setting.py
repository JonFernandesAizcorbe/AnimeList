import os

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from flask import redirect
from sqlalchemy.orm import Session

from app.auth.dependencies import user_require
from app.database import get_db
from app.models.user import UserORM

router = APIRouter(prefix="/setting", tags=["setting"])
templates = Jinja2Templates(directory="app/templates")


import uuid
import magic  # Valida Magic Numbers
import aiofiles  # Escribe archivos de forma asíncrona
from pathlib import Path
from fastapi import File, UploadFile, HTTPException, status



# Configuraciones de seguridad
UPLOAD_DIR = Path("app/static/uploads/")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_TYPES = {"image/jpeg": ".jpg", "image/png": ".png"}

@router.post("/upload/")
async def upload_image(
    request: Request, 
    file: UploadFile = File(...), 
    user: UserORM = Depends(user_require),
    db: Session = Depends(get_db)
):
    if not user:
        raise HTTPException(status_code=401, detail="Necesitas estar registrado")

    # 1. Validaciones de seguridad (Tamaño y tipo)
    file_content = await file.read(MAX_FILE_SIZE + 1)
    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="Archivo demasiado grande")
    
    detected_mime = magic.from_buffer(file_content, mime=True)
    if detected_mime not in ALLOWED_TYPES:
        raise HTTPException(status_code=415, detail="Tipo de archivo no permitido")
    
    # 2. BORRADO DE LA IMAGEN ANTERIOR (Si existe)
    # Suponiendo que el campo en tu base de datos se llama 'avatar'
    if user.image:
        old_file_path = UPLOAD_DIR / user.image
        try:
            # Comprobamos si el archivo realmente existe físicamente en el disco
            if old_file_path.exists() and old_file_path.is_file():
                os.remove(old_file_path)  # Elimina el archivo viejo
        except Exception as e:
            # Es buena práctica registrar el error (log) pero no detener la ejecución, 
            # así el usuario puede subir su nueva foto de todos modos.
            print(f"Error al eliminar archivo antiguo: {e}")

    # 3. Generar nuevo nombre seguro
    safe_name = f"{uuid.uuid4()}{ALLOWED_TYPES[detected_mime]}"
    
    # 4. Almacenamiento FÍSICO de la nueva imagen
    async with aiofiles.open(UPLOAD_DIR / safe_name, "wb") as f:
        await f.write(file_content)

    # 5. Actualizar la BASE DE DATOS con el nuevo nombre
    user.image = safe_name
    db.add(user)
    db.commit()
    db.refresh(user)

    return RedirectResponse(url="/setting", status_code=303)



@router.get("", response_class=HTMLResponse)
def setting(request: Request, db: Session = Depends(get_db), user: UserORM = Depends(user_require)):

    return templates.TemplateResponse(
        "profile/setting.html",
        {"request": request, "user": user}
    )
