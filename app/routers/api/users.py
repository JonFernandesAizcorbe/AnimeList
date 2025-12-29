from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session


from app.database import get_db
from app.models.user import UserORM
from app.schemas.user import UserCreate, UserPatch, UserResponse


router = APIRouter(prefix="/api/user", tags=["users"])

@router.get("", response_model=list[UserResponse])
def list_user(db: Session = Depends(get_db)):
    users = db.execute(select(UserORM)).scalars().all()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - No hay usuarios en base de datos")

    return users

@router.get("/{id}", response_model=UserResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"404 - El usuario con id {id} no existe")
    
    return user

@router.post("", response_model=UserResponse)
def create_user(user_dto: UserCreate, db: Session = Depends(get_db)):

    new_user = UserORM(
        user_name=user_dto.user_name,
        email=user_dto.email,
        password=user_dto.password,
        description=user_dto.description,
        image=user_dto.image
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.patch("/{id}", response_model=UserResponse)
def update_user(id: int, user_dto: UserPatch, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - El usuario con id {id} no existe")
    
    update_data = user_dto.model_dump()

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    user = db.execute(select(UserORM).where(UserORM.id == id)).scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="404 - El usuario con id {id} no existe")
    
    db.delete(user)
    db.commit()

    return None