from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class TagBase(BaseModel):
    """Базовая схема тега"""
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#9b59b6", pattern="^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    """Схема для создания тега"""
    pass


class TagUpdate(BaseModel):
    """Схема для обновления тега"""
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")


class TagResponse(TagBase):
    """Схема ответа с данными тега"""
    id: int
    owner_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class TagInTask(BaseModel):
    """Схема тега внутри задачи"""
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True

