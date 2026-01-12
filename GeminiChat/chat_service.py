from utils.chat_history import add_message, get_history
from google import genai
from google.genai.errors import ClientError
import os, asyncio
from dotenv import load_dotenv
from utils.prompt import build_prompt

load_dotenv()
os.environ["GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
client = genai.Client()

async def generate_with_retry(prompt, retries=3):
    for _ in range(retries):
        try:
            response = await asyncio.to_thread(
                client.models.generate_content,
                model="gemini-3-flash-preview",
                contents=prompt
)

            return response.text
        except ClientError as e:
            if hasattr(e, "code") and e.code == 429:
                print("Rate limit hit, retrying in 5 seconds...")
                await asyncio.sleep(5)
            else:
                raise
    return "AI unavailable. Try again later."

async def get_ai_response(message: str):
    add_message("User", message)

    prompt = build_prompt(get_history())
    ai_message = await generate_with_retry(prompt)

    add_message("AI", ai_message)
    return ai_message

