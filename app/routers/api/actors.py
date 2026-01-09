from fastapi import APIRouter, Depends, HTTPException, status
from app.database import get_db
from app.models.actor import ActorORM
from app.schemas.actor import ActorResponse, ActorCreate, ActorPatch
from sqlalchemy.orm import Session
from sqlalchemy import select

router = APIRouter(prefix="/api/actor", tags=["actors"])


@router.get("", response_model=list[ActorResponse])
def list_actor(db: Session = Depends(get_db)):
    actors = db.execute(select(ActorORM)).scalars().all()

    if not actors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - No hay actores en la base de datos")
    
    return actors

@router.get("/{id}", response_model=ActorResponse)
def find_id(id: int, db: Session = Depends(get_db)):
    actor =  db.execute(select(ActorORM).where(ActorORM.id == id)).scalar_one_or_none()

    if actor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - El actor con id {id} no existe")
    
    return actor

@router.post("", response_model=ActorResponse)
def create_actor(actor_dto: ActorCreate, db: Session = Depends(get_db)):
    new_actor = ActorORM(
        name=actor_dto.name,
        description=actor_dto.description,
        image=actor_dto.image
    )

    db.add(new_actor)
    db.commit()
    db.refresh(new_actor)

    return new_actor

@router.patch("/{id}", response_model=ActorResponse)
def update(id: int, actor_dto: ActorPatch, db: Session = Depends(get_db)):
    actor = db.execute(select(ActorORM).where(ActorORM.id == id)).scalar_one_or_none()

    if actor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - El actor con id {id} no existe")
    
    update_data = actor_dto.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(actor, field, value)

    db.commit()
    db.refresh(actor)

    return actor

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    actor = db.execute(select(ActorORM).where(ActorORM.id == id)).scalar_one_or_none()

    if actor is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - El actor con id {id} no existe")
    
    db.delete(actor)
    db.commit()
    
    return None