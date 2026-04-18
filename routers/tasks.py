# Updated routers/tasks.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter()

@router.get("/tasks/{task_id}")
async def get_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}")
async def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task.dict().items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    db_task = db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == current_user.id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    db.commit()
    return {"detail": "Task deleted successfully"}

@router.get("/tasks/")
async def get_all_tasks(db: Session = Depends(get_db), current_user: str = Depends(get_current_user)):
    tasks = db.query(models.Task).filter(models.Task.owner_id == current_user.id).all()
    return tasks
