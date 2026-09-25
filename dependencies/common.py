from fastapi import Query
from pydantic import BaseModel
from database.database import SessionLocal

class ApplicationSettings(BaseModel):
    app_name: str
    version: str
    environment: str
    debug: bool

class PaginationParams(BaseModel):
    page: int
    limit: int

def get_settings() -> ApplicationSettings:
    return ApplicationSettings(
        app_name="FastAPI User Management",
        version="1.0",
        environment="development",
        debug=True,
    )

def get_pagination(
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
) -> PaginationParams:
    return PaginationParams(
        page=page,
        limit=limit,
    )

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
