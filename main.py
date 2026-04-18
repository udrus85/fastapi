from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from routers import tasks, users, auth

app = FastAPI(
    title="Your API",
    description="Your API description",
    version="1.0.0",
)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Your API",
        version="1.0.0",
        description="Your API description",
        routes=app.routes,
    )

    # Добавляем security scheme для Bearer токена
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Применяем ко всем endpoints кроме /auth/login
    for path, path_item in openapi_schema.get("paths", {}).items():
        for method, operation in path_item.items():
            if isinstance(operation, dict):
                # Не добавляем security для endpoints создания пользователя и логина
                if "login" not in path and "create_user" not in path:
                    operation.setdefault("security", []).append({"bearerAuth": []})

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi
