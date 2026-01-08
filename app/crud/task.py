from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc, or_, func, and_
from typing import Optional, List
from datetime import datetime, timedelta

from app.models.models import Task, TaskStatus, TaskPriority, Tag
from app.schemas.task import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    """Получить задачу по ID с тегами"""
    return db.query(Task).options(joinedload(Task.tags)).filter(
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
    category_id: Optional[int] = None,
    is_favorite: Optional[bool] = None,
    tag_ids: Optional[List[int]] = None,
    search_query: Optional[str] = None,
    overdue: Optional[bool] = None
) -> tuple[List[Task], int]:
    """Получить список задач с расширенной фильтрацией"""
    query = db.query(Task).options(joinedload(Task.tags)).filter(Task.owner_id == owner_id)

    # Фильтры
    if status:
        query = query.filter(Task.status == status)
    if priority:
        query = query.filter(Task.priority == priority)
    if category_id:
        query = query.filter(Task.category_id == category_id)
    if is_favorite is not None:
        query = query.filter(Task.is_favorite == is_favorite)

    # Фильтр по тегам
    if tag_ids:
        query = query.filter(Task.tags.any(Tag.id.in_(tag_ids)))

    # Полнотекстовый поиск
    if search_query:
        search_pattern = f"%{search_query}%"
        query = query.filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern),
                Task.notes.ilike(search_pattern)
            )
        )

    # Просроченные задачи
    if overdue is True:
        query = query.filter(
            and_(
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.DONE,
                Task.status != TaskStatus.CANCELLED
            )
        )

    # Общее количество (без дублей из-за joinedload)
    count_query = db.query(Task).filter(Task.owner_id == owner_id)
    if status:
        count_query = count_query.filter(Task.status == status)
    if priority:
        count_query = count_query.filter(Task.priority == priority)
    if category_id:
        count_query = count_query.filter(Task.category_id == category_id)
    if is_favorite is not None:
        count_query = count_query.filter(Task.is_favorite == is_favorite)
    if tag_ids:
        count_query = count_query.filter(Task.tags.any(Tag.id.in_(tag_ids)))
    if search_query:
        search_pattern = f"%{search_query}%"
        count_query = count_query.filter(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern),
                Task.notes.ilike(search_pattern)
            )
        )
    if overdue is True:
        count_query = count_query.filter(
            and_(
                Task.due_date < datetime.utcnow(),
                Task.status != TaskStatus.DONE,
                Task.status != TaskStatus.CANCELLED
            )
        )

    total = count_query.count()

    # Сортировка и пагинация
    tasks = query.order_by(desc(Task.is_favorite), desc(Task.created_at)).offset(skip).limit(limit).all()

    # Удаляем дубликаты из-за joinedload
    seen = set()
    unique_tasks = []
    for task in tasks:
        if task.id not in seen:
            seen.add(task.id)
            unique_tasks.append(task)

    return unique_tasks, total


def create_task(db: Session, task: TaskCreate, owner_id: int, tags: List[Tag] = None) -> Task:
    """Создать задачу"""
    task_data = task.model_dump(exclude={'tag_ids'})
    db_task = Task(
        **task_data,
        owner_id=owner_id
    )

    if tags:
        db_task.tags = tags

    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session,
    task_id: int,
    task_update: TaskUpdate,
    owner_id: int,
    tags: List[Tag] = None
) -> Optional[Task]:
    """Обновить задачу"""
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return None

    update_data = task_update.model_dump(exclude_unset=True, exclude={'tag_ids'})

    # Если статус меняется на DONE, записываем время завершения
    if "status" in update_data and update_data["status"] == TaskStatus.DONE:
        update_data["completed_at"] = datetime.utcnow()

    # Если статус меняется с DONE на другой, убираем время завершения
    if "status" in update_data and update_data["status"] != TaskStatus.DONE:
        update_data["completed_at"] = None

    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Обновляем теги если переданы
    if tags is not None:
        db_task.tags = tags

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


def toggle_favorite(db: Session, task_id: int, owner_id: int) -> Optional[Task]:
    """Переключить избранное"""
    db_task = get_task(db, task_id, owner_id)
    if not db_task:
        return None

    db_task.is_favorite = not db_task.is_favorite
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_stats(db: Session, owner_id: int) -> dict:
    """Получить расширенную статистику по задачам"""
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
    cancelled = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.status == TaskStatus.CANCELLED
    ).count()

    # Просроченные
    overdue = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.due_date < datetime.utcnow(),
        Task.status != TaskStatus.DONE,
        Task.status != TaskStatus.CANCELLED
    ).count()

    # Избранные
    favorites = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.is_favorite == True
    ).count()

    # С напоминаниями
    with_reminders = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.reminder_at != None
    ).count()

    # Статистика по приоритетам
    priority_stats = {}
    for priority in TaskPriority:
        count = db.query(Task).filter(
            Task.owner_id == owner_id,
            Task.priority == priority
        ).count()
        priority_stats[priority.value] = count

    # Задачи на сегодня
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    due_today = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.due_date >= today_start,
        Task.due_date < today_end,
        Task.status != TaskStatus.DONE,
        Task.status != TaskStatus.CANCELLED
    ).count()

    # Задачи на эту неделю
    week_end = today_start + timedelta(days=7)
    due_this_week = db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.due_date >= today_start,
        Task.due_date < week_end,
        Task.status != TaskStatus.DONE,
        Task.status != TaskStatus.CANCELLED
    ).count()

    # Процент выполнения
    completion_rate = round((done / total * 100), 1) if total > 0 else 0

    return {
        "total": total,
        "by_status": {
            "todo": todo,
            "in_progress": in_progress,
            "done": done,
            "cancelled": cancelled
        },
        "by_priority": priority_stats,
        "overdue": overdue,
        "favorites": favorites,
        "with_reminders": with_reminders,
        "due_today": due_today,
        "due_this_week": due_this_week,
        "completion_rate": completion_rate
    }


def get_upcoming_reminders(db: Session, owner_id: int, hours: int = 24) -> List[Task]:
    """Получить задачи с напоминаниями в ближайшие N часов"""
    now = datetime.utcnow()
    future = now + timedelta(hours=hours)

    return db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.reminder_at >= now,
        Task.reminder_at <= future,
        Task.status != TaskStatus.DONE,
        Task.status != TaskStatus.CANCELLED
    ).order_by(Task.reminder_at).all()


def get_overdue_tasks(db: Session, owner_id: int) -> List[Task]:
    """Получить просроченные задачи"""
    return db.query(Task).options(joinedload(Task.tags)).filter(
        Task.owner_id == owner_id,
        Task.due_date < datetime.utcnow(),
        Task.status != TaskStatus.DONE,
        Task.status != TaskStatus.CANCELLED
    ).order_by(Task.due_date).all()
