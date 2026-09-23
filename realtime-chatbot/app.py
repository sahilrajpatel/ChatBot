"""
API version of the chatbot.
Run with: uvicorn app:app --reload
Then open http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from pydantic import BaseModel
from langchain_core.messages import HumanMessage

from src.chatbot_graph import build_graph

app = FastAPI(title="Realtime Chatbot")
graph = build_graph()


class Message(BaseModel):
    message: str


@app.get("/")
def home():
    return {"status": "Chatbot API is running. Go to /docs to try it."}


@app.post("/chat")
def chat(data: Message):
    result = graph.invoke({"messages": [HumanMessage(content=data.message)]})
    reply = result["messages"][-1].content
    return {"reply": reply}
