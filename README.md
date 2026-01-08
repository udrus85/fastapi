# 📋 FastAPI Task Manager

REST API для управления задачами с аутентификацией пользователей, построенное на FastAPI.

## 🚀 Возможности

- ✅ Регистрация и аутентификация пользователей (JWT)
- ✅ CRUD операции для задач
- ✅ Категории и теги для организации
- ✅ Приоритеты и статусы задач
- ✅ Избранные задачи ⭐
- ✅ Напоминания и дедлайны 🔔
- ✅ Полнотекстовый поиск 🔍
- ✅ Расширенная фильтрация
- ✅ Статистика и аналитика 📊
- ✅ Экспорт в CSV 📁
- ✅ Автоматическая документация API (Swagger/ReDoc)

## 📁 Структура проекта

```
fastapi-task-manager/
├── app/
│   ├── api/           # API endpoints
│   │   ├── auth.py    # Аутентификация
│   │   ├── users.py   # Пользователи
│   │   ├── tasks.py   # Задачи
│   │   ├── categories.py # Категории
│   │   └── tags.py    # Теги
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
- `GET /api/v1/tasks` - Список задач (с поиском и фильтрами)
- `POST /api/v1/tasks` - Создать задачу
- `GET /api/v1/tasks/{id}` - Получить задачу
- `PUT /api/v1/tasks/{id}` - Обновить задачу
- `DELETE /api/v1/tasks/{id}` - Удалить задачу
- `POST /api/v1/tasks/{id}/favorite` - Добавить в избранное
- `GET /api/v1/tasks/stats` - Статистика
- `GET /api/v1/tasks/overdue` - Просроченные задачи
- `GET /api/v1/tasks/reminders` - Напоминания
- `GET /api/v1/tasks/export/csv` - Экспорт в CSV

### Категории
- `GET /api/v1/categories` - Список категорий
- `POST /api/v1/categories` - Создать категорию
- `PUT /api/v1/categories/{id}` - Обновить категорию
- `DELETE /api/v1/categories/{id}` - Удалить категорию

### Теги
- `GET /api/v1/tags` - Список тегов
- `POST /api/v1/tags` - Создать тег
- `PUT /api/v1/tags/{id}` - Обновить тег
- `DELETE /api/v1/tags/{id}` - Удалить тег

## 🔍 Примеры использования

### Регистрация
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "username": "user", "password": "password123"}'
```

### Создание задачи с тегами
```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Важная задача",
    "description": "Описание задачи",
    "priority": "high",
    "is_favorite": true,
    "tag_ids": [1, 2],
    "due_date": "2026-01-15T18:00:00"
  }'
```

### Поиск задач
```bash
curl "http://localhost:8000/api/v1/tasks?search=важная&is_favorite=true" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Получение статистики
```bash
curl "http://localhost:8000/api/v1/tasks/stats" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📊 Статистика возвращает:
```json
{
  "total": 25,
  "by_status": {
    "todo": 10,
    "in_progress": 5,
    "done": 8,
    "cancelled": 2
  },
  "by_priority": {
    "low": 5,
    "medium": 12,
    "high": 6,
    "urgent": 2
  },
  "overdue": 3,
  "favorites": 7,
  "due_today": 2,
  "due_this_week": 8,
  "completion_rate": 32.0
}
```

## 🛠 Технологии

- **FastAPI** - Современный веб-фреймворк
- **SQLAlchemy** - ORM для работы с БД
- **Pydantic** - Валидация данных
- **JWT** - Аутентификация
- **Uvicorn** - ASGI сервер
- **SQLite** - База данных (легко заменить на PostgreSQL)

## 📝 Лицензия

MIT License
