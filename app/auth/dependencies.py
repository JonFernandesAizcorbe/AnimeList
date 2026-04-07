
# CREAR UN SECRET TOKEN
# python -c "import secrets; print(secrets.token_urlsafe(64))"

from fastapi import Request, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import UserORM


def get_current_user(request: Request, db: Session = Depends(get_db)) -> UserORM | None: 
    
    user_id = request.session.get("user_id")

    if not user_id:
        return None

    user = db.get(UserORM, user_id)

    if not user:
        request.session.clear()
        return None

    return user

def user_require(user: UserORM | None = Depends(get_current_user)) -> UserORM | None:
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sin autorización")
    return user
