from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api import api_router


# Создание таблиц в БД
Base.metadata.create_all(bind=engine)

# Создание приложения FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="""
## 📋 Task Manager API

REST API для управления задачами с аутентификацией пользователей.

### Возможности:
- ✅ Регистрация и аутентификация пользователей (JWT)
- ✅ CRUD операции для задач
- ✅ Категории задач с цветовой маркировкой
- ✅ Приоритеты и статусы задач
- ✅ Фильтрация и пагинация
- ✅ Статистика по задачам

### Аутентификация:
Используйте `/api/v1/auth/login` для получения JWT токена.
Добавляйте токен в заголовок `Authorization: Bearer <token>` для защищённых endpoints.
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "Аутентификация", "description": "Регистрация и вход в систему"},
        {"name": "Пользователи", "description": "Управление профилем пользователя"},
        {"name": "Задачи", "description": "CRUD операции с задачами"},
        {"name": "Категории", "description": "Управление категориями задач"},
    ]
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене укажите конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(api_router)


@app.get("/", tags=["Root"])
async def root():
    """
    Корневой endpoint API
    """
    return {
        "message": "Welcome to Task Manager API",
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """
    Проверка состояния API
    """
    return {"status": "healthy"}
