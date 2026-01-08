from fastapi import APIRouter

from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.tasks import router as tasks_router
from app.api.categories import router as categories_router
from app.api.tags import router as tags_router


# Главный роутер API
api_router = APIRouter(prefix="/api/v1")

# Подключаем все роутеры
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(tasks_router)
api_router.include_router(categories_router)
api_router.include_router(tags_router)

