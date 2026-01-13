from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routes.chat_routes import router as chat_router
from utils.koha_client import koha_health_check


app = FastAPI()

# Root route for health check
@app.get("/")
def home():
    return {"message": "AI Chatbot API is running."}

# Include all chat routes from chat_routes.py
app.include_router(chat_router)

@app.get("/koha/test")
def koha_test():
    result = koha_health_check()  # synchronous call
    if not isinstance(result, dict):
        # safety fallback
        result = {"status": "fail", "message": "Koha health check returned unexpected value"}
        return JSONResponse(status_code=500, content=result)
    if result.get("status") != "ok":
        return JSONResponse(status_code=500, content=result)
    return result