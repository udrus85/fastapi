# routers/users.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import crud.users as crud_users
from database import get_db
from dependencies.auth import get_current_user
import schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud_users.create_user(db, user)


@router.get("/", response_model=list[schemas.User])
def read_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)  # ← ДОБАВЬТЕ
):
    return crud_users.read_users(db)