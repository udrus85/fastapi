from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.schemas.tag import TagCreate, TagUpdate, TagResponse
from app.crud.tag import (
    get_tag,
    get_tags,
    get_tag_by_name,
    create_tag,
    update_tag,
    delete_tag
)


router = APIRouter(prefix="/tags", tags=["Теги"])


@router.get("", response_model=List[TagResponse])
async def list_tags(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить все теги текущего пользователя
    """
    return get_tags(db, current_user.id)


@router.post("", response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_new_tag(
    tag: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Создать новый тег

    - **name**: Название тега (уникальное для пользователя)
    - **color**: HEX цвет (например, #9b59b6)
    """
    # Проверяем уникальность имени
    existing = get_tag_by_name(db, tag.name, current_user.id)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Тег с таким именем уже существует"
        )

    return create_tag(db, tag, current_user.id)


@router.get("/{tag_id}", response_model=TagResponse)
async def get_tag_by_id(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить тег по ID
    """
    tag = get_tag(db, tag_id, current_user.id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тег не найден"
        )
    return tag


@router.put("/{tag_id}", response_model=TagResponse)
async def update_tag_by_id(
    tag_id: int,
    tag_update: TagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить тег
    """
    # Проверяем уникальность имени если меняется
    if tag_update.name:
        existing = get_tag_by_name(db, tag_update.name, current_user.id)
        if existing and existing.id != tag_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Тег с таким именем уже существует"
            )

    tag = update_tag(db, tag_id, tag_update, current_user.id)
    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тег не найден"
        )
    return tag


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag_by_id(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Удалить тег
    """
    if not delete_tag(db, tag_id, current_user.id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тег не найден"
        )

