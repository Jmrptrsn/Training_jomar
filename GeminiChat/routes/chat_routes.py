from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from chat_service import get_ai_response
from utils.chat_history import get_history, reset_history

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/test")
async def test():
    return {"message": "Hello from chat_routes"}

@router.post("/")
async def chat(message: str = Form(...)):
    ai_message = await get_ai_response(message)
    return JSONResponse({"message": ai_message})

@router.get("/history")
async def history():
    return {"chat_history": get_history()}

@router.post("/reset")
async def reset():
    reset_history()
    return {"message": "Chat history cleared"}
    