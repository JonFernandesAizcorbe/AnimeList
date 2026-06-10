from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.auth.dependencies import user_require
from app.database import get_db
from app.models.user import UserORM

router = APIRouter(prefix="/setting", tags=["setting"])
templates = Jinja2Templates(directory="app/templates")


@router.get("", response_class=HTMLResponse)
def setting(request: Request, db: Session = Depends(get_db), user: UserORM = Depends(user_require)):

    return templates.TemplateResponse(
        "profile/setting.html",
        {"request": request, "user": user}
    )
