from sqlalchemy.orm import Session, joinedload
from utils.security import hash_password

import models
import schemas


def create_user(
        db: Session,
        user: schemas.UserCreate
):
    hashed_password = hash_password(
        user.password
    )

    db_user = models.User(
        username=user.username,
        hashed_password=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def read_users(
        db: Session
):
    return db.query(models.User).all()


def get_user_tasks(
        db: Session,
        user_id: int
):
    user = (
        db.query(models.User)
        .options(joinedload(models.User.tasks))
        .filter(models.User.id == user_id)
        .first()
    )

    if not user:
        return None

    return user.tasks