from fastapi import FastAPI
from fastapi.openapi.models import APIKey, APIKeyIn

app = FastAPI(
    title="Your API Title",
    description="Your API Description",
    version="1.0.0",
    openapi_tags=[
        {"name": "tag_name", "description": "Tag description"},
    ],
)

# Define a security scheme
app.openapi_schema = {
    "openapi": "3.0.2",
    "info": {
        "title": "Your API Title",
        "version": "1.0.0",
        "description": "Your API Description"
    },
    "paths": {},
    "components": {
        "securitySchemes": {
            "BearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    },
}

# Apply Bearer token security scheme
@app.get("/secure-endpoint", tags=["tag_name"], security=[{"BearerAuth": []}])
def secure_endpoint():
    return {"message": "This is a secured endpoint"}