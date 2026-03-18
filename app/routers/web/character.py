from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.character import CharacterORM
from app.models.user_character import user_character_table
from app.models.user import UserORM


templates = Jinja2Templates(directory="app/templates")
router = APIRouter(prefix="/character", tags=["web"])

@router.get("/{character_id}", response_class=HTMLResponse)
def character_info(request: Request, character_id: int, db: Session = Depends(get_db), user: UserORM = Depends(get_current_user)):
    character = db.execute(select(CharacterORM).where(CharacterORM.id == character_id)).scalar_one_or_none()
    follows = db.execute(select(func.count(user_character_table.c.user_id)).where(user_character_table.c.character_id == character_id)).scalar()
    

    if character:
        return templates.TemplateResponse(
            "detail/character.html",
            {"request": request, "character": character, "user": user, "follows": follows}
        )
    else:
        raise HTTPException(status_code=404, detail="Character not found")
    

@router.post("/follow", response_class=HTMLResponse)
def follow_character(
    request: Request,
    character_id: int = Form(...),
    db: Session = Depends(get_db),
    user: UserORM = Depends(get_current_user)
):
    
    character = db.get(CharacterORM, character_id)


    if character in user.characters:
        user.characters.remove(character)
    
    else:
        user.characters.append(character)

    
    db.commit()
    db.refresh(user)

    return RedirectResponse(url=f"/character/{character_id}", status_code=303)
    


      