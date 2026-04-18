# routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import crud.tasks as crud_tasks
from schemas import Task, TaskCreate, TaskUpdate
from dependencies.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=Task)
def create_task(
        task: TaskCreate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)  # ← ДОБАВЬТЕ
):
    return crud_tasks.create_task(db, task)


@router.get("/")
def read_tasks(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    return crud_tasks.get_tasks(db)


@router.get("/me")
def me(user=Depends(get_current_user)):
    return user
