

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.actor import ActorORM
from app.models.user import UserORM
from app.models.user_actor import users_actors_table

router = APIRouter(prefix="/actor", tags=["actor"])
templates = Jinja2Templates(directory="app/templates")

@router.get("/{actor_id}", response_class=HTMLResponse)
def actor_detail(
    request: Request,
    actor_id: int,
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):
    
    actor = db.execute(select(ActorORM).where(ActorORM.id == actor_id)).scalar_one_or_none()
    follows = db.execute(select(func.count(users_actors_table.c.user_id)).where(users_actors_table.c.actor_id == actor_id)).scalar()

    return templates.TemplateResponse(
        "detail/character.html",
        {"request": request, "actor": actor, "follows": follows, "user": user }
    )

@router.post("/follow", response_class=HTMLResponse)
def follow_actor(
    request: Request,
    actor_id: int = Form(...),
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):
    
    actor = db.get(ActorORM, actor_id)

    if not user:
        return RedirectResponse(url=f"/actor/{actor_id}", status_code=303)
    
    if actor in user.actors:
        user.actors.remove(actor)
    else:
        user.actors.append(actor)

    
    db.commit()
    db.refresh(user)

    return RedirectResponse(url=f"/actor/{actor_id}", status_code=303)
            

        