# main.py
from fastapi import FastAPI, Depends
from routers import tasks, users, auth

app = FastAPI(
    title="Your API",
    description="Your API description",
    version="1.0.0",
)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)