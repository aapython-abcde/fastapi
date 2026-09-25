import asyncio
import httpx
from fastapi import (
    APIRouter,
    HTTPException,
    Path,
    Query,
    status,
    Depends
)
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
    prefix="/mcp",
    tags=["MCP"],
)

@router.get("/async-demo")
async def async_demo():
    await asyncio.sleep(5)

    return {
    "message":
    "Completed"
    }

@router.get("/quote")
async def quote():
    async with httpx.AsyncClient() as client:
        response = await client.get(
        "https://echoes.soferity.com/api/quotes/random"
    )
    return response.json()

