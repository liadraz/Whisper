from bs4 import BeautifulSoup
from typing import Optional
import httpx

BASE_URL = "https://books.toscrape.com/"


def get_genre_slug_map():
    """
    Scrape genre navigation bar and return a dict:
    normalized genre name (e.g., "science") → slug (e.g., "science_22")
    """
    html = fetch_book_page()
    soup = BeautifulSoup(html, "html.parser")
    
    mapping = {}
    
    nav_links = soup.select("ul.nav-list ul > li > a")
    
    for link in nav_links:
        genre = ' '.join(link.text.strip().split()).lower()
        href = link["href"]

        slug = href.split("/")[-2]
        mapping["genre"] = slug
    
    return mapping


def fetch_book_page(url: Optional[str] = None):
    
    if not url or not url.strip():
        url = BASE_URL
    
    headers = {
        "User-Agent": "Mozilla/5.0" 
    }
    
    response = httpx.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")

    return response.text


def scrape_books(genre_slug: Optional[str] = None):
    """
    Scrapes books from a specific genre.
    Returns list of dicts: title, price, link
    """
    html = fetch_book_page(genre_slug)
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
