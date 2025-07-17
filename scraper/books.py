from functools import lru_cache
from bs4 import BeautifulSoup
from typing import Optional

import httpx


BASE_URL = "https://books.toscrape.com/"

def build_url(genre: Optional[str]) -> str:
    """
    Build the URL for a given book genre on books.toscrape.com.

    If no genre is provided, returns the main catalog URL.
    Otherwise, retrieves the genre slug from the mapped dict and constructs the corresponding category URL.
    """
    if genre is None:
        return BASE_URL
    
    mapping = get_genre_slug_map()
    
    slug = mapping.get(genre)
    if not slug:
        raise ValueError(f"Genre '{genre}' not found in genre mapping.")
    
    return f"{BASE_URL}/catalogue/category/books/{slug}/index.html"


def scrape_books(genre_url: Optional[str]):
    """
    Scrapes books from a specific genre or the main catalog if no genre is provided.
    Returns a list of dictionaries containing: title, price, and link.
    """
    if genre_url is None:
        genre_url = BASE_URL

    html = fetch_page(genre_url)
    soup = BeautifulSoup(html, "html.parser")
    
    results = []
    
    books = soup.select("article.product_pod")

    for book in books:
        title = book.h3.a["title"]
        
        raw_price = book.select_one(".price_color").text.strip()
        price = float(raw_price.replace('£', '')) 
        
        href = book.h3.a["href"]
        link = BASE_URL + href.replace('../../../', '')
        
        book_data = {
            "title": title,
            "price": price,
            "link": link
        }
        
        results.append(book_data)
    
    return results


def fetch_page(url: str):
    
    if url is None:
        raise ValueError("Error: cannot fetch invalid url")
            
    headers = { "User-Agent": "Mozilla/5.0" }
    
    response = httpx.get(url, headers=headers)

    if response.status_code != 200:
        raise httpx.HTTPStatusError(f"Request failed with status {response.status_code}")

    return response.text


@lru_cache()
def get_genre_slug_map():
    """
    Scrape genre navigation bar and return a dict:
    normalized genre name (e.g., "science") → slug (e.g., "science_22")
    """
    html = fetch_page(BASE_URL)
    soup = BeautifulSoup(html, "html.parser")
    
    mapping = {}
    
    nav_links = soup.select("ul.nav-list ul > li > a")
    
    for link in nav_links:
        genre = ' '.join(link.text.strip().split()).lower()
        href = link["href"]

        slug = href.split("/")[-2]
        mapping[genre] = slug
    
    return mapping
