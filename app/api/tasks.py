from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.models import User, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskListResponse
from app.crud.task import (
    get_task,
    get_tasks,
    create_task,
    update_task,
    delete_task,
    get_tasks_stats
)


router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество на странице"),
    status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу"),
    priority: Optional[TaskPriority] = Query(None, description="Фильтр по приоритету"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список задач с фильтрацией и пагинацией

    Параметры фильтрации:
    - **status**: todo, in_progress, done, cancelled
    - **priority**: low, medium, high, urgent
    - **category_id**: ID категории
    """
    skip = (page - 1) * per_page
    tasks, total = get_tasks(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=per_page,
        status=status,
        priority=priority,
        category_id=category_id
    )

    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        per_page=per_page
    )


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создать новую задачу

    - **title**: Заголовок задачи (обязательно)
    - **description**: Описание задачи
    - **priority**: Приоритет (low, medium, high, urgent)
    - **due_date**: Срок выполнения
    - **category_id**: ID категории
    """
    return create_task(db, task, current_user.id)


@router.get("/stats")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить статистику по задачам

    Возвращает количество задач по статусам
    """
    return get_tasks_stats(db, current_user.id)


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить задачу по ID
    """
    task = get_task(db, task_id, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task


@router.put("/{task_id}", response_model=TaskResponse)
async def update_task_by_id(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить задачу

    Можно обновить любые поля:
    - **title**, **description**, **priority**, **status**, **due_date**, **category_id**
    """
    task = update_task(db, task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_by_id(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить задачу
    """
    if not delete_task(db, task_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )

