from fastapi import APIRouter


router = APIRouter(prefix="/api/animes", tags=["animes"])

@router.get("", response_model=)