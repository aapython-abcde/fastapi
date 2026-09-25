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

from services.openai_service import (
ask_openai
)

router = APIRouter(
    prefix="/chat",
    tags=["Chatbot"],
)

class ChatRequest(
    BaseModel
):
    prompt: str


@router.post("")
async def chat(
    request: ChatRequest
):
    answer = ask_openai(
    request.prompt
    )
    return {
        "response":
        answer
    }