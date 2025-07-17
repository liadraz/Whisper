from models import DialogFlowRequest
from typing import Optional

from scraper.books import build_url, scrape_books

# Webhook request parameters
GENRE = "genre"
PRICE_LIMIT = "price_limit"

def books_handler(body: DialogFlowRequest):

    genre = parse_text(body.queryResult.parameters.get(GENRE))
    price_limit = parse_price(body.queryResult.parameters.get(PRICE_LIMIT))
    
    books = scrape_books(build_url(genre))
    
    results = []
    
    for book in books:
        if price_limit is None or book["price"] <= price_limit:
            results.append(book)
    
    if not results:
        return "Sorry, no books found matching your criteria."
    
    lines = [
        f"{i + 1}. {book["title"]} - ${book["price"]:.2f} - {book["link"]}"
        for i, book in enumerate(results)
    ]
    
    return f"Here are some books for you:\n {'\n'.join(lines)}"


def parse_text(value: Optional[str]) -> Optional[str]:
    return value.strip().lower() if value and value.strip() else None

def parse_price(raw: Optional[str]) -> Optional[float]:
    if not raw:
        return None
    try:
        return float(raw)
    except (ValueError, TypeError):
        return None