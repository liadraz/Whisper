from models import DialogFlowRequest
from scraper import scrape_books, get_genre_slug_map

def books_handler(body: DialogFlowRequest):

    raw_genre = body.queryResult.parameters.get("genre")
    genre = raw_genre.strip().lower() if raw_genre else None
    
    slug_map = get_genre_slug_map()
    genre_slug = slug_map.get(genre) if genre else None
    
    books = scrape_books(genre_slug)
    
    raw_price = body.queryResult.parameters.get("price_limit")
    
    if raw_price in (None, ""):
        price_limit = None
    else:
        try:
            price_limit = float(raw_price)
        except ValueError:
            price_limit = None
    
    results = []
    for book in books:
        if price_limit is None or book["price"] <= price_limit:
            results.append(book)
    
    if not results:
        return "Sorry, no books found matching your criteria."
    
    lines = [
        f"{i + 1}. {book["title"]} - ${book["price"]:.2f} - {book["genre"]} - {book["link"]}"
        for i, book in enumerate(results)
    ]
    
    return f"Here are some books for you:\n {'\n'.join(lines)}"
    

# title
# price
# genre
# product link