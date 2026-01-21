
# CREAR UN SECRET TOKEN
# python -c "import secrets; print(secrets.token_urlsafe(64))"

from fastapi import Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import UserORM


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserORM: 
    
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.get(UserORM, user_id)

    if not user:
        request.session.clear()
        return None

    return user
