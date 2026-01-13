from utils.chat_history import add_message, get_history
from google import genai
from google.genai.errors import ClientError
import os, asyncio
from dotenv import load_dotenv
from utils.prompt import build_prompt
from chat_koha import get_available_books_from_koha




load_dotenv()
os.environ["GENAI_API_KEY"] = os.getenv("GEMINI_API_KEY")
client = genai.Client()

# -------------------------------
# AI functions
# -------------------------------
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

# -------------------------------
# Main chatbot loop
# -------------------------------
async def main():
    while True:
        user_input = input("You: ")
        if user_input.lower() in ("exit", "quit"):
            break

        # First, try Koha
        availability_keywords = ["available", "other books", "show books", "what books"]

        if any(word in user_input.lower() for word in availability_keywords):
    # Fetch general available books from Koha
            koha_response = get_available_books_from_koha(limit=5)
            print("Library Bot:", koha_response)
        else:
    # Normal search
            koha_response = get_available_books_from_koha(limit=5, query=user_input)
            if "couldn't find any books" not in koha_response:
                print("Library Bot:", koha_response)
            else:
        # Fallback to AI
                ai_response = await get_ai_response(user_input)
                print("AI:", ai_response)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nGoodbye! 👋 Chatbot stopped by user.")
