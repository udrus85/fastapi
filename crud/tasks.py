from sqlalchemy.orm import Session, joinedload
import models
import schemas


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        completed=False,
        user_id=task.user_id
    )

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


def get_tasks(db: Session):
    return (
        db.query(models.Task)
        .options(joinedload(models.Task.user))
        .all()
    )


def get_task(db: Session, task_id: int):
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id)
        .first()
    )


def update_task(db: Session, task_id: int, completed: bool):
    task = get_task(db, task_id)

    if task:
        task.completed = completed
        db.commit()
        db.refresh(task)

    return task


def delete_task(db: Session, task_id: int):
    task = get_task(db, task_id)

    if task:
        db.delete(task)
        db.commit()

    return task


def get_task_with_user(db: Session, task_id: int):
    return (
        db.query(models.Task)
        .options(joinedload(models.Task.user))
        .filter(models.Task.id == task_id)
        .first()
    )
