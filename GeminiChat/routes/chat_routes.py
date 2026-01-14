from fastapi import APIRouter, Form
from fastapi.responses import JSONResponse
from chat_service import get_ai_response
from utils.chat_history import add_message, get_history, reset_history
from chat_koha import get_available_books_from_koha

router = APIRouter(prefix="/chat", tags=["Chat"])

availability_keywords = ["available", "other books", "show books", "what books"]

@router.post("/")
async def chat(message: str = Form(...)):
    # Record the user's message
    add_message("User", message)

    if any(word in message.lower() for word in availability_keywords):
        koha_response = get_available_books_from_koha(limit=5)
    else:
        koha_response = get_available_books_from_koha(limit=5, query=message)

    # Fallback to AI only if Koha found nothing
    if isinstance(koha_response, str) and "couldn't find" in koha_response.lower():
        ai_response = await get_ai_response(message)
        return JSONResponse({"message": ai_response})

    # Record Koha response
    add_message("Library Bot", koha_response)
    return JSONResponse({"message": koha_response})

@router.get("/history")
async def history():
    return {"chat_history": get_history()}

@router.post("/reset")
async def reset():
    reset_history()
    return {"message": "Chat history cleared"}
