from pydantic import BaseModel


class TaskBase(BaseModel):
    title: str
    completed: bool = False
    user_id: int


class TaskCreate(BaseModel):
    title: str
    user_id: int


class TaskUpdate(BaseModel):
    completed: bool


class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


class Task(BaseModel):
    id: int
    title: str
    completed: bool
    user_id: int
    user: User

    class Config:
        from_attributes = True
