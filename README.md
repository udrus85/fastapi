# 📋 FastAPI Task Manager

REST API для управления задачами с аутентификацией пользователей, построенное на FastAPI.

## 🚀 Возможности

- ✅ Регистрация и аутентификация пользователей (JWT)
- ✅ CRUD операции для задач
- ✅ Категории задач
- ✅ Приоритеты и статусы задач
- ✅ Фильтрация и сортировка
- ✅ Автоматическая документация API (Swagger/ReDoc)
- ✅ Валидация данных с Pydantic
- ✅ SQLite/PostgreSQL база данных

## 📁 Структура проекта

```
fastapi-task-manager/
├── app/
│   ├── api/           # API endpoints
│   ├── core/          # Конфигурация и безопасность
│   ├── crud/          # Операции с базой данных
│   ├── models/        # SQLAlchemy модели
│   ├── schemas/       # Pydantic схемы
│   └── main.py        # Точка входа
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/fastapi-task-manager.git
cd fastapi-task-manager
```

2. Создайте виртуальное окружение:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Создайте файл `.env` из примера:
```bash
cp .env.example .env
```

5. Отредактируйте `.env` и установите свой секретный ключ:
```
SECRET_KEY=your-super-secret-key
```

## 🚀 Запуск

```bash
uvicorn app.main:app --reload
```

API будет доступно по адресу: http://localhost:8000

## 📚 Документация API

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 🔐 API Endpoints

### Аутентификация
- `POST /api/v1/auth/register` - Регистрация пользователя
- `POST /api/v1/auth/login` - Вход в систему

### Пользователи
- `GET /api/v1/users/me` - Текущий пользователь
- `PUT /api/v1/users/me` - Обновить профиль

### Задачи
- `GET /api/v1/tasks` - Список задач
- `POST /api/v1/tasks` - Создать задачу
- `GET /api/v1/tasks/{id}` - Получить задачу
- `PUT /api/v1/tasks/{id}` - Обновить задачу
- `DELETE /api/v1/tasks/{id}` - Удалить задачу

### Категории
- `GET /api/v1/categories` - Список категорий
- `POST /api/v1/categories` - Создать категорию
- `DELETE /api/v1/categories/{id}` - Удалить категорию

## 🧪 Примеры запросов

### Регистрация
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "password123"}'
```

### Создание задачи
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Моя первая задача", "description": "Описание", "priority": "high"}'
```

## 🛠 Технологии

- **FastAPI** - Современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - Валидация данных
- **JWT** - Аутентификация
- **Uvicorn** - ASGI сервер

## 📝 Лицензия

MIT License

