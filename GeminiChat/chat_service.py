from google import genai
from google.genai.errors import ClientError
import os, time
from dotenv import load_dotenv

load_dotenv()
os.environ["GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
client = genai.Client()

chat_history = []
MAX_HISTORY = 10

def generate_with_retry(prompt, retries=3):
    for i in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=prompt
            )
            return response.text
        except ClientError as e:
            if hasattr(e, "code") and e.code ==429:
                wait_time = 45
                print(f"Rate limited. Waiting {wait_time}s...")
                time.sleep(wait_time)
            else:
                print("f'ClientError: {e}")
                raise 
    return "AI unavailable. Try again later."

def get_ai_response(message: str):
    chat_history.append(f"User: {message}")
    if len(chat_history) > MAX_HISTORY:
        chat_history[:] = chat_history[-MAX_HISTORY:]

    full_prompt = "You are a helpful chatbot.\n" + "\n".join(chat_history)
    ai_message = generate_with_retry(full_prompt)
    chat_history.append(f"AI: {ai_message}")
    return ai_message

def get_chat_history():
    return chat_history

def reset_chat_history():
    chat_history.clear()
