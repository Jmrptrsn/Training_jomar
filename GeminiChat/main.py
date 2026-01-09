from fastapi import FastAPI
from routes.chat_routes import router as chat_router


app = FastAPI()

# Root route for health check
@app.get("/")
def home():
    return {"message": "AI Chatbot API is running."}

# Include all chat routes from chat_routes.py
app.include_router(chat_router)
