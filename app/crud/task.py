from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List
from datetime import datetime

from app.models.models import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    """Получить задачу по ID"""
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == owner_id
    ).first()


def get_tasks(
    db: Session,
    owner_id: int,
    skip: int = 0,
    limit: int = 10,
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    category_id: Optional[int] = None
) -> tuple[List[Task], int]:
    """Получить список задач с фильтрацией"""
    query = db.query(Task).filter(Task.owner_id == owner_id)

    # Фильтры
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category_id:
        query = query.filter(Task.category_id == category_id)

    # Общее количество
    total = query.count()

    # Сортировка и пагинация
    tasks = query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()

    return tasks, total


def create_task(db: Session, task: TaskCreate, owner_id: int) -> Task:
    """Создать задачу"""
    db_task = Task(
        **task.model_dump(),
        owner_id=owner_id
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate, owner_id: int) -> Optional[Task]:
    """Обновить задачу"""
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True)

    # Если статус меняется на DONE, записываем время завершения
    if "status" in update_data and update_data["status"] == TaskStatus.DONE:
        update_data["completed_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    """Удалить задачу"""
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return False

    db.delete(db_task)
    db.commit()
    return True


def get_tasks_stats(db: Session, owner_id: int) -> dict:
    """Получить статистику по задачам"""
    total = db.query(Task).filter(Task.owner_id == owner_id).count()
    done = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.status == TaskStatus.DONE
    ).count()
    in_progress = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.status == TaskStatus.IN_PROGRESS
    ).count()
    todo = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.status == TaskStatus.TODO
    ).count()

    return {
        "total": total,
        "done": done,
        "in_progress": in_progress,
        "todo": todo
    }

