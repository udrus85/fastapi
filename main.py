# main.py
from fastapi import FastAPI, Depends
from routers import tasks, users, auth
from dependencies.auth import oauth2_scheme

app = FastAPI(
    title="Your API",
    description="Your API description",
    version="1.0.0",
    dependencies=[Depends(oauth2_scheme)]  # ← Добавьте эту строку
)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)