from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from chat_service import get_ai_response, get_chat_history, reset_chat_history

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.get("/test")
async def test():
    return {"message": "Hello from chat_routes"}

@router.post("/")
def chat(message: str = Form(...)):
    ai_message = get_ai_response(message)
    return JSONResponse({"message": ai_message})

@router.get("/history")
def history():
    return {"chat_history": get_chat_history()}

@router.post("/reset")
def reset():
    reset_chat_history()
    return {"message": "Chat history cleared"}
