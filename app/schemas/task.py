from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TaskPriority(str, Enum):
    """Приоритет задачи"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class TaskStatus(str, Enum):
    """Статус задачи"""
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"


class TagInTask(BaseModel):
    """Тег внутри задачи"""
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True


class TaskBase(BaseModel):
    """Базовая схема задачи"""
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None
    reminder_at: Optional[datetime] = None
    is_favorite: bool = False
    estimated_hours: Optional[int] = Field(None, ge=1, le=1000)
    notes: Optional[str] = Field(None, max_length=10000)
    tag_ids: Optional[List[int]] = None


class TaskCreate(TaskBase):
    """Схема для создания задачи"""
    pass


class TaskUpdate(BaseModel):
    """Схема для обновления задачи"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=5000)
    priority: Optional[TaskPriority] = None
    status: Optional[TaskStatus] = None
    due_date: Optional[datetime] = None
    category_id: Optional[int] = None
    reminder_at: Optional[datetime] = None
    is_favorite: Optional[bool] = None
    estimated_hours: Optional[int] = Field(None, ge=1, le=1000)
    notes: Optional[str] = Field(None, max_length=10000)
    tag_ids: Optional[List[int]] = None


class TaskResponse(BaseModel):
    """Схема ответа с данными задачи"""
    id: int
    title: str
    description: Optional[str]
    priority: TaskPriority
    status: TaskStatus
    due_date: Optional[datetime]
    reminder_at: Optional[datetime]
    is_favorite: bool
    estimated_hours: Optional[int]
    notes: Optional[str]
    owner_id: int
    category_id: Optional[int]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    tags: List[TagInTask] = []

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    """Схема для списка задач с пагинацией"""
    tasks: List[TaskResponse]
    total: int
    page: int
    per_page: int


class TaskSearchParams(BaseModel):
    """Параметры поиска задач"""
    query: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None
    is_favorite: Optional[bool] = None
    has_due_date: Optional[bool] = None
    overdue: Optional[bool] = None
