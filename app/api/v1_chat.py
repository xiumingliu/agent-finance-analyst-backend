from fastapi import APIRouter, HTTPException
from ..state import df as GLOBAL_DF, SESSIONS
from ..services.agent import build_agent, capture_plot_as_base64_if_any
from langchain.memory import ConversationBufferMemory
from ..core.config import settings
from pydantic import BaseModel
from typing import List, Optional
from .. import state

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    session_id: Optional[str] = None

router = APIRouter()

@router.post("/chat")
def chat(req: ChatRequest):
    if not settings.openai_api_key:
        raise HTTPException(status_code=503, detail="OPENAI_API_KEY not configured")

    df = state.df
    if df is None:
        raise HTTPException(500, "Dataframe not loaded")

    sid = req.session_id or "default"
    memory = SESSIONS.get(sid)
    if memory is None:
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        SESSIONS[sid] = memory
        # optional seed from earlier turns (if client sends)
        for m in req.messages[:-1]:
            (memory.chat_memory.add_user_message if m.sender == "user" else memory.chat_memory.add_ai_message)(m.text)

    agent = build_agent(df, memory, settings.openai_model)
    latest = req.messages[-1].text if req.messages else ""
    result = agent.invoke({"input": latest})
    text = result.get("output", str(result))
    plot_b64 = capture_plot_as_base64_if_any()

    return {"reply": text, "plot": plot_b64}