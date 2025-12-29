from sys import prefix
from fastapi import FastAPI


router = FastAPI(prefix="/api/users", tags=["users"])

