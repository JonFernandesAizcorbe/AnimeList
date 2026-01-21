from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.database import get_db
from app.models.user import UserORM
from app.security.passwords import verify_password

router = APIRouter(tags=["auth"])
templates = Jinja2Templates(directory="app/templates")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login/login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    
    user_by_email = db.query(UserORM).filter(UserORM.email == email).first()
    user_by_user_name = db.query(UserORM).filter(UserORM.user_name == email).first()

    user = user_by_email or user_by_user_name


    errors = []

    value_data = {}

    if not user or not verify_password(password, user.password_hash):
        errors.append("Credenciales incorrectas")
    else:
        value_data = {
            "email": email
        } 

    if errors:
        return templates.TemplateResponse(
            "login/login.html",
            {"request": request, "errors": errors, "value_data": value_data}
        )

    request.session["user_id"] = user.id

    return RedirectResponse(url="/", status_code=303)

@router.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/", status_code=302)



