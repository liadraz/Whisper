from bs4 import BeautifulSoup
import httpx

BASE_URL = "https://books.toscrape.com/"


def get_genre_slug_map():
    """
    Scrape genre navigation bar and return a dict:
    normalized genre name (e.g., "science") → slug (e.g., "science_22")
    """
    html = fetch_base_page()
    soup = BeautifulSoup(html, "html.parser")
    
    mapping = {}
    
    nav_links = soup.select("ul.nav-list ul > li > a")
    
    for link in nav_links:
        name = ' '.join(link.text.strip().split()).lower()
        href = link["href"]

        slug = href.split("/")[-2]
        mapping["name"] = slug
    
    return mapping


def fetch_base_page():
    
    headers = {
        "User-Agent": "Mozilla/5.0" 
    }
    
    response = httpx.get(BASE_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Request failed with status {response.status_code}")

    return response.text


def scrape_books(genre_slug: str):
    html = fetch_base_page()
    soup = BeautifulSoup(html, "html.parser")
    
    results = []
    
    books = soup.select("article.product_pod")

    for book in books[:5]:
        title = book.h3.a["title"]
        price = book.select_one(".price_color").text.strip()
        results.append(f"{title} - {price}")
    
    return results

print(get_genre_slug_map())