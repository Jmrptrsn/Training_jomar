from utils.koha_client import search_books_by_title, fetch_items
import json

def get_available_books_from_koha(limit=5, query=""):
    """
    Search Koha for books matching user input.
    Returns a readable response for the chatbot.
    """
    books = search_books_by_title(query)

    if not books:
        return "Sorry, I couldn't find any books matching your query."

    response_lines = []
    for book in books[:limit]:  # limit to first 5 results
        title = book.get("title")
        author = book.get("author")
        biblio_id = book.get("biblio_id")
        items = fetch_items(biblio_id)

        # Count available items (robust check for field variations)
        available_items = sum(
            1 for item in items
            if item.get("status", "").lower() == "available"
               or item.get("item_status", "").lower() == "available"
        ) if items else 0

        # Build the line inside the loop
        line = f"📚 {title} by {author}"
        if available_items > 0:
            line += f" - {available_items} available"
        else:
            line += " - currently not available"

        response_lines.append(line)

    return "\n".join(response_lines)
