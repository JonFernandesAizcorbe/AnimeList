from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.auth.validators import validate_email_format
from app.database import get_db
from app.models.user import UserORM
from app.security.passwords import hash_password


templates = Jinja2Templates(directory="app/templates")

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/create")
def register(request: Request):
    return templates.TemplateResponse(
        "login/register.html",
        {"request": request}
    )



@router.post("/create", response_class=HTMLResponse)
def create_user(
    request: Request,
    user_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    errors = []

# check if user_name is empty or is duplicate
    if not user_name or not user_name.strip():
        errors.append("El nombre de usuario no puede estar vacío")

    name_exist = db.execute(select(UserORM).where(UserORM.user_name == user_name)).scalar_one_or_none()

    if name_exist:
        errors.append("Ya existe un usuario con este nombre")
    
# check email
    
    if not email or not email.strip():
        errors.append("El correo electrónico no puede estar vacío")
    
    email_exist = db.execute(select(UserORM).where(UserORM.email == email)).scalar_one_or_none()

    if email_exist:
        errors.append("Ya existe una cuenta con este correo electrónico")

    value_email = validate_email_format(email)

    if value_email is None:
        errors.append("Email inválido")

# validate password and hash

    if not password or not password.strip():
        errors.append("La contraseña no puede estar vacía")
    
    if len(password) < 8:
        errors.append("La contraseña tiene que contener 8 caráteres")

    if errors:
        return templates.TemplateResponse(
            "login/register.html",
            {"request": request, "errors": errors}
        )

    
    pwd = hash_password(password)


    try:
        new_user = UserORM(
            user_name=user_name,
            email=value_email,
            password_hash=pwd
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

    except Exception:
        db.rollback()
        errors.append("Se ha producido un error al crear el usuario")

        return templates.TemplateResponse(
            "login/register.html",
            {"request": request, "errors": errors}
        )

    



        
        



