from typing import Optional
from models.dialogflow_request import DialogFlowRequest
from scraper.books_scraper import build_url, scrape_books
from utils.string_utils import parse_text, parse_float

# Webhook request parameters
GENRE = "genre"
PRICE_LIMIT = "price_limit"

def books_handler(body: DialogFlowRequest):

    genre = parse_text(body.queryResult.parameters.get(GENRE))
    price_limit = parse_float(body.queryResult.parameters.get(PRICE_LIMIT))
    
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


