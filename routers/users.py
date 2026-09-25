from fastapi import File, UploadFile
from fastapi import BackgroundTasks
import time
import os
from security.auth import (
   hash_password,
   verify_password,
   create_access_token
)
from fastapi import Header
from dependencies.common import (
    ApplicationSettings,
    PaginationParams,
    get_pagination,
    get_settings,
)

from typing import Optional
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    Depends
)
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
)
from sqlalchemy.orm import Session
from dependencies.common import get_db

from database.models import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/info")
def get_application_info(
    settings: ApplicationSettings = Depends(get_settings),
):
    return settings


class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )
    email: EmailStr
    age: int = Field(
        gt=0,
        lt=120,
    )
    phone: Optional[str] = None
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    phone: Optional[str] = None

users = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john.doe@example.com",
        "age": 40,
        "phone": "+971500000001",
    },
    {
        "id": 2,
        "name": "Mary Smith",
        "email": "mary.smith@example.com",
        "age": 35,
        "phone": None,
    },
    {
        "id": 3,
        "name": "David Lee",
        "email": "david.lee@example.com",
        "age": 29,
        "phone": "+971500000003",
    },
]

@router.get("/profile")
def profile(authorization: str | None = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"message": "Protected Route"}

@router.post("", response_model=UserResponse)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = User(
        name=user.name,
        email=user.email,
        age=user.age,
        phone=user.phone,
        password_hash=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("", response_model=list[UserResponse])
def get_users(
    search: Optional[str] = Query(default=None, min_length=1),
    pagination: PaginationParams = Depends(get_pagination),
    db: Session = Depends(get_db),
):
    filtered_users = db.query(User).all()

    if search:
        search_text = search.lower()
        filtered_users = [
            user
            for user in filtered_users
            if search_text in user.name.lower()
            or search_text in user.email.lower()
        ]

    start = (pagination.page - 1) * pagination.limit
    end = start + pagination.limit
    return filtered_users[start:end]

class LoginRequest(BaseModel):
   email: EmailStr
   password: str

@router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(request.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(user.email)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

ALLOWED_EXTENSIONS = [".pdf", ".docx", ".xlsx", ".csv"]

def process_document(filename: str):
    with open("logs/processing.log", "a") as log:
        log.write(f"{filename} processed\n")

@router.get("/processing-log")
def processing_log():
    with open("logs/processing.log", "r") as log:
        content = log.readlines()
    return {"entries": content}

@router.post("/upload")
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    filepath = os.path.join("uploads", file.filename)

    with open(filepath, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    background_tasks.add_task(process_document, file.filename)
    return {"message": "File uploaded", "filename": file.filename}


@router.get("/files")
def get_files():
    files = os.listdir("uploads")
    return {"files": files}


@router.get("/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(ge=1),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )
    return user
