from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
from google import genai
import os
from dotenv import load_dotenv
import time
from google.genai.errors import ClientError

load_dotenv()
os.environ["GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
client = genai.Client()

chat_history = []
MAX_HISTORY = 10

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AI Chatbot API is running."}


@app.post("/chat")
def chat(message: str = Form(...)):
    chat_history.append(f"User: {message}")
    
    if len(chat_history) > MAX_HISTORY:
        chat_history[:] = chat_history[-MAX_HISTORY:]

    full_prompt = "\n".join(chat_history)
    full_prompt = f"You are a helpful chatbot.\n{full_prompt}"

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=full_prompt
    )
    
    ai_message = response.text
    chat_history.append(f"AI: {ai_message}")
    return JSONResponse(content={"johnny": ai_message})

@app.get("/history")
def get_history():
    return {"chat_history": chat_history}

@app.post("/reset")
def reset_history():
    chat_history.clear()
    return {"message": "chat history is cleared"}

@app.get("/routes")
def list_routes():
    return {"routes": [route.path for route in app.routes]}

def generate_with_retry(model, prompt, retries=3):
    for i in range(retries):
        try:
            return model.generate_content(prompt)
        except ClientError as e:
            if e.status_code == 429:
                wait_time = 45
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e