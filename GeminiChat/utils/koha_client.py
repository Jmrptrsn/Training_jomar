import os
import json
import base64
import requests
from dotenv import load_dotenv
from cachetools import TTLCache


load_dotenv()

KOHA_API_URL = os.getenv("KOHA_BASE_URL")        # read value from .env
USERNAME     = os.getenv("KOHA_API_USER")       # read value from .env
PASSWORD     = os.getenv("KOHA_API_PASSWORD") 
TIMEOUT = 10  # seconds

search_cache = TTLCache(maxsize=1000, ttl=300) #cache global
search_cache["test"] = "ok"
print(search_cache["test"])

# -------------------------------
# Helper: Basic Auth headers
# -------------------------------
def get_auth_headers():
    """Return headers with Basic Auth for Koha API."""
    auth_str = f"{USERNAME}:{PASSWORD}"
    token = base64.b64encode(auth_str.encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
def test_connection():
    url = f"{KOHA_API_URL}/biblios"  # endpoint to test
    headers = get_auth_headers()
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            print("Connection successful! ✅")
            print("Sample response:", json.dumps(response.json()[:1], indent=2))  # show first record
        else:
            print(f"Unexpected status code: {response.status_code}")
            print(response.text)
    except Exception as e:
        print("Connection failed ❌", e)

if __name__ == "__main__":
    test_connection()

# -------------------------------
# Helper: GET request
# -------------------------------
def koha_get(endpoint, params=None):
    """Make a GET request to Koha API."""
    url = f"{KOHA_API_URL}{endpoint}"
    headers = get_auth_headers()
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        response.raise_for_status()  # raise error if status != 200
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e} - {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    return None

# -------------------------------
# Search biblios by title
# -------------------------------
def search_books_by_title(title):
    cache_key = title.lower().strip()

    # 1️⃣ Check cache first
    if cache_key in search_cache:
        print("⚡ Cache hit")
        return search_cache[cache_key]

    print("🌐 Calling Koha API")
    query = {"title": {"-like": f"%{title}%"}}
    result = koha_get("/biblios", params={"q": json.dumps(query)})

    # 2️⃣ Save to cache
    if result:
        search_cache[cache_key] = result

    return result


# -------------------------------
# Fetch items for a biblio_id
# -------------------------------
def fetch_items(biblio_id):
    return koha_get(f"/biblios/{biblio_id}/items")

# -------------------------------
# Example usage
# -------------------------------
if __name__ == "__main__":
    # Search for books with "Python" in the title
    print("\n--- First call ---")
    books = search_books_by_title("Python")

    print("\n--- Second call ---")
    books = search_books_by_title("Python")

    if books:
        print("Books found:")
        print(json.dumps(books, indent=2))

        # Fetch items for the first book
        biblio_id = books[0]["biblio_id"]
        items = fetch_items(biblio_id)
        if items:
            print(f"\nItems for biblio_id {biblio_id}:")
            print(json.dumps(items, indent=2))
        else:
            print("No items found for this biblio_id.")
    else:
        print("No books found with that title.")

def koha_health_check():
    """Check if Koha API is reachable and returning data."""
    try:
        data = koha_get("/biblios")  # don't pass `limit=1` if Koha API doesn't accept it
        if data:
            return {"status": "ok", "message": "Koha API is reachable"}
        else:
            return {"status": "fail", "message": "Koha API returned no data"}
    except Exception as e:
        return {"status": "fail", "message": str(e)}
    
    


