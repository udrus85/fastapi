from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import Optional, List
import csv
import io
from datetime import datetime

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
    get_tasks_stats,
    toggle_favorite,
    get_upcoming_reminders,
    get_overdue_tasks
)
from app.crud.tag import get_tags_by_ids


router = APIRouter(prefix="/tasks", tags=["Задачи"])


@router.get("", response_model=TaskListResponse)
async def list_tasks(
    page: int = Query(1, ge=1, description="Номер страницы"),
    per_page: int = Query(10, ge=1, le=100, description="Количество на странице"),
    status: Optional[TaskStatus] = Query(None, description="Фильтр по статусу"),
    priority: Optional[TaskPriority] = Query(None, description="Фильтр по приоритету"),
    category_id: Optional[int] = Query(None, description="Фильтр по категории"),
    is_favorite: Optional[bool] = Query(None, description="Только избранные"),
    tag_ids: Optional[str] = Query(None, description="ID тегов через запятую"),
    search: Optional[str] = Query(None, description="Поиск по тексту"),
    overdue: Optional[bool] = Query(None, description="Только просроченные"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить список задач с расширенной фильтрацией и поиском

    Параметры фильтрации:
    - **status**: todo, in_progress, done, cancelled
    - **priority**: low, medium, high, urgent
    - **category_id**: ID категории
    - **is_favorite**: Только избранные (true/false)
    - **tag_ids**: ID тегов через запятую (например: 1,2,3)
    - **search**: Поиск по названию, описанию и заметкам
    - **overdue**: Только просроченные задачи
    """
    skip = (page - 1) * per_page

    # Парсим tag_ids если переданы
    parsed_tag_ids = None
    if tag_ids:
        try:
            parsed_tag_ids = [int(x.strip()) for x in tag_ids.split(",")]
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный формат tag_ids. Используйте числа через запятую."
            )

    tasks, total = get_tasks(
        db,
        owner_id=current_user.id,
        skip=skip,
        limit=per_page,
        status=status,
        priority=priority,
        category_id=category_id,
        is_favorite=is_favorite,
        tag_ids=parsed_tag_ids,
        search_query=search,
        overdue=overdue
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
    - **reminder_at**: Время напоминания
    - **category_id**: ID категории
    - **tag_ids**: Список ID тегов
    - **is_favorite**: Добавить в избранное
    - **estimated_hours**: Оценка времени в часах
    - **notes**: Дополнительные заметки
    """
    # Получаем теги если указаны
    tags = None
    if task.tag_ids:
        tags = get_tags_by_ids(db, task.tag_ids, current_user.id)

    return create_task(db, task, current_user.id, tags)


@router.get("/stats")
async def get_statistics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить расширенную статистику по задачам

    Возвращает:
    - Общее количество задач
    - Распределение по статусам и приоритетам
    - Количество просроченных, избранных, с напоминаниями
    - Задачи на сегодня и эту неделю
    - Процент выполнения
    """
    return get_tasks_stats(db, current_user.id)


@router.get("/reminders")
async def get_reminders(
    hours: int = Query(24, ge=1, le=168, description="Часов вперед"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить задачи с напоминаниями в ближайшие N часов
    """
    return get_upcoming_reminders(db, current_user.id, hours)


@router.get("/overdue", response_model=List[TaskResponse])
async def get_overdue(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все просроченные задачи
    """
    return get_overdue_tasks(db, current_user.id)


@router.get("/export/csv")
async def export_tasks_csv(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Экспортировать все задачи в CSV файл
    """
    tasks, _ = get_tasks(db, owner_id=current_user.id, skip=0, limit=10000)

    # Создаем CSV в памяти
    output = io.StringIO()
    writer = csv.writer(output)

    # Заголовки
    writer.writerow([
        "ID", "Название", "Описание", "Статус", "Приоритет",
        "Срок", "Избранное", "Оценка (часы)", "Создано", "Обновлено"
    ])

    # Данные
    for task in tasks:
        writer.writerow([
            task.id,
            task.title,
            task.description or "",
            task.status.value,
            task.priority.value,
            task.due_date.isoformat() if task.due_date else "",
            "Да" if task.is_favorite else "Нет",
            task.estimated_hours or "",
            task.created_at.isoformat(),
            task.updated_at.isoformat()
        ])

    output.seek(0)

    filename = f"tasks_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )


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

    Можно обновить любые поля, включая теги через tag_ids
    """
    # Получаем теги если указаны
    tags = None
    if task_update.tag_ids is not None:
        tags = get_tags_by_ids(db, task_update.tag_ids, current_user.id)

    task = update_task(db, task_id, task_update, current_user.id, tags)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задача не найдена"
        )
    return task


@router.post("/{task_id}/favorite", response_model=TaskResponse)
async def toggle_task_favorite(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Переключить статус избранного для задачи
    """
    task = toggle_favorite(db, task_id, current_user.id)
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
