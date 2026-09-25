from fastapi import FastAPI
from database.database import Base, engine
from routers.users import router as users_router
from routers.mcpdemo import router as mcp_router
from routers.chatbot import router as chat_router
import gradio as gr
from gradio_app import demo

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users_router)
app.include_router(mcp_router)
app.include_router(chat_router)

app = gr.mount_gradio_app(
    app,
    demo,
    "/gradio"
)
