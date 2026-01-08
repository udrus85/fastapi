from sqlalchemy.orm import Session
from typing import Optional, List

from app.models.models import Category
from app.schemas.category import CategoryCreate, CategoryUpdate


def get_category(db: Session, category_id: int, owner_id: int) -> Optional[Category]:
    """Получить категорию по ID"""
    return db.query(Category).filter(
        Category.id == category_id,
        Category.owner_id == owner_id
    ).first()


def get_categories(db: Session, owner_id: int) -> List[Category]:
    """Получить все категории пользователя"""
    return db.query(Category).filter(Category.owner_id == owner_id).all()


def create_category(db: Session, category: CategoryCreate, owner_id: int) -> Category:
    """Создать категорию"""
    db_category = Category(
        **category.model_dump(),
        owner_id=owner_id
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def update_category(
    db: Session,
    category_id: int,
    category_update: CategoryUpdate,
    owner_id: int
) -> Optional[Category]:
    """Обновить категорию"""
    db_category = get_category(db, category_id, owner_id)
    if not db_category:
        return None

    update_data = category_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(db_category, field, value)

    db.commit()
    db.refresh(db_category)
    return db_category


def delete_category(db: Session, category_id: int, owner_id: int) -> bool:
    """Удалить категорию"""
    db_category = get_category(db, category_id, owner_id)
    if not db_category:
        return False

    db.delete(db_category)
    db.commit()
    return True

