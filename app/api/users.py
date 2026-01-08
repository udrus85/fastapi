from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.models import User
from app.schemas.user import UserResponse, UserUpdate
from app.crud.user import update_user, get_user_by_email, get_user_by_username


router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    Получить информацию о текущем пользователе
    """
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Обновить данные текущего пользователя

    Можно обновить:
    - **email**: Новый email
    - **username**: Новое имя пользователя
    - **password**: Новый пароль
    """
    # Проверяем уникальность email
    if user_update.email and user_update.email != current_user.email:
        if get_user_by_email(db, user_update.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email уже используется"
            )

    # Проверяем уникальность username
    if user_update.username and user_update.username != current_user.username:
        if get_user_by_username(db, user_update.username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Имя пользователя уже занято"
            )

    updated_user = update_user(db, current_user.id, user_update)
    return updated_user

