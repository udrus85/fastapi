from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.models import Tag
from app.schemas.tag import TagCreate, TagUpdate


def get_tag(db: Session, tag_id: int, owner_id: int) -> Optional[Tag]:
    """Получить тег по ID"""
    return db.query(Tag).filter(
        Tag.id == tag_id,
        Tag.owner_id == owner_id
    ).first()


def get_tags(db: Session, owner_id: int) -> List[Tag]:
    """Получить все теги пользователя"""
    return db.query(Tag).filter(Tag.owner_id == owner_id).all()


def get_tag_by_name(db: Session, name: str, owner_id: int) -> Optional[Tag]:
    """Получить тег по имени"""
    return db.query(Tag).filter(
        Tag.name == name,
        Tag.owner_id == owner_id
    ).first()


def create_tag(db: Session, tag: TagCreate, owner_id: int) -> Tag:
    """Создать тег"""
    db_tag = Tag(
        **tag.model_dump(),
        owner_id=owner_id
    )
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def update_tag(
    db: Session,
    tag_id: int,
    tag_update: TagUpdate,
    owner_id: int
) -> Optional[Tag]:
    """Обновить тег"""
    db_tag = get_tag(db, tag_id, owner_id)
    if not db_tag:
        return None

    update_data = tag_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_tag, field, value)

    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, tag_id: int, owner_id: int) -> bool:
    """Удалить тег"""
    db_tag = get_tag(db, tag_id, owner_id)
    if not db_tag:
        return False

    db.delete(db_tag)
    db.commit()
    return True


def get_tags_by_ids(db: Session, tag_ids: List[int], owner_id: int) -> List[Tag]:
    """Получить теги по списку ID"""
    return db.query(Tag).filter(
        Tag.id.in_(tag_ids),
        Tag.owner_id == owner_id
    ).all()

