import pytest
from unittest.mock import patch, Mock
from bs4 import BeautifulSoup
import httpx

from scraper.books_scraper import (
    build_url, 
    scrape_books, 
    fetch_page, 
    get_genre_slug_map,
    BASE_URL
)


class TestBuildUrl:
    """Test cases for build_url function"""
    
    def test_build_url_no_genre(self):
        """Test build_url with no genre returns base URL"""
        result = build_url(None)
        assert result == BASE_URL
    
    @patch('scraper.books_scraper.get_genre_slug_map')
    def test_build_url_valid_genre(self, mock_get_genre_slug_map):
        """Test build_url with valid genre"""
        mock_get_genre_slug_map.return_value = {'fiction': 'fiction_10'}
        
        result = build_url('fiction')
        expected = f"{BASE_URL}/catalogue/category/books/fiction_10/index.html"
        
        assert result == expected
        mock_get_genre_slug_map.assert_called_once()
    
    @patch('scraper.books_scraper.get_genre_slug_map')
    def test_build_url_invalid_genre(self, mock_get_genre_slug_map):
        """Test build_url with invalid genre raises ValueError"""
        mock_get_genre_slug_map.return_value = {'fiction': 'fiction_10'}
        
        with pytest.raises(ValueError, match="Genre 'nonexistent' not found in genre mapping."):
            build_url('nonexistent')


class TestFetchPage:
    """Test cases for fetch_page function"""
    
    def test_fetch_page_none_url(self):
        """Test fetch_page with None URL raises ValueError"""
        with pytest.raises(ValueError, match="Error: cannot fetch invalid url"):
            fetch_page(None)
    
    @patch('httpx.get')
    def test_fetch_page_success(self, mock_get):
        """Test fetch_page with successful response"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"
        mock_get.return_value = mock_response
        
        result = fetch_page("https://example.com")
        
        assert result == "<html><body>Test content</body></html>"
        mock_get.assert_called_once_with(
            "https://example.com", 
            headers={"User-Agent": "Mozilla/5.0"}
        )
    
    @patch('httpx.get')
    def test_fetch_page_http_error(self, mock_get):
        """Test fetch_page with HTTP error status"""
        mock_request = Mock()
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.request = mock_request
        mock_get.return_value = mock_response
        
        with pytest.raises(httpx.HTTPStatusError, match="Request failed with status 404"):
            fetch_page("https://example.com")


class TestScrapeBooks:
    """Test cases for scrape_books function"""
    
    @patch('scraper.books_scraper.fetch_page')
    def test_scrape_books_none_url(self, mock_fetch_page):
        """Test scrape_books with None URL uses BASE_URL"""
        mock_html = """
        <html>
            <body>
                <article class="product_pod">
                    <h3><a title="Test Book" href="../../../catalogue/test-book_1/index.html">Test Book</a></h3>
                    <p class="price_color">£12.99</p>
                </article>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        result = scrape_books(None)
        
        mock_fetch_page.assert_called_once_with(BASE_URL)
        assert len(result) == 1
        assert result[0]['title'] == 'Test Book'
        assert result[0]['price'] == 12.99
        assert result[0]['link'] == BASE_URL + 'catalogue/test-book_1/index.html'
    
    @patch('scraper.books_scraper.fetch_page')
    def test_scrape_books_with_url(self, mock_fetch_page):
        """Test scrape_books with specific URL"""
        test_url = "https://books.toscrape.com/catalogue/category/books/fiction_10/index.html"
        mock_html = """
        <html>
            <body>
                <article class="product_pod">
                    <h3><a title="Fiction Book" href="../../../catalogue/fiction-book_1/index.html">Fiction Book</a></h3>
                    <p class="price_color">£15.50</p>
                </article>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        result = scrape_books(test_url)
        
        mock_fetch_page.assert_called_once_with(test_url)
        assert len(result) == 1
        assert result[0]['title'] == 'Fiction Book'
        assert result[0]['price'] == 15.50
        assert result[0]['link'] == BASE_URL + 'catalogue/fiction-book_1/index.html'
    
    @patch('scraper.books_scraper.fetch_page')
    def test_scrape_books_multiple_books(self, mock_fetch_page):
        """Test scrape_books with multiple books"""
        mock_html = """
        <html>
            <body>
                <article class="product_pod">
                    <h3><a title="Book One" href="../../../catalogue/book-one_1/index.html">Book One</a></h3>
                    <p class="price_color">£10.00</p>
                </article>
                <article class="product_pod">
                    <h3><a title="Book Two" href="../../../catalogue/book-two_2/index.html">Book Two</a></h3>
                    <p class="price_color">£20.99</p>
                </article>
                <article class="product_pod">
                    <h3><a title="Book Three" href="../../../catalogue/book-three_3/index.html">Book Three</a></h3>
                    <p class="price_color">£5.25</p>
                </article>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        result = scrape_books("https://example.com")
        
        assert len(result) == 3
        
        # Check first book
        assert result[0]['title'] == 'Book One'
        assert result[0]['price'] == 10.00
        assert result[0]['link'] == BASE_URL + 'catalogue/book-one_1/index.html'
        
        # Check second book
        assert result[1]['title'] == 'Book Two'
        assert result[1]['price'] == 20.99
        assert result[1]['link'] == BASE_URL + 'catalogue/book-two_2/index.html'
        
        # Check third book
        assert result[2]['title'] == 'Book Three'
        assert result[2]['price'] == 5.25
        assert result[2]['link'] == BASE_URL + 'catalogue/book-three_3/index.html'
    
    @patch('scraper.books_scraper.fetch_page')
    def test_scrape_books_no_books(self, mock_fetch_page):
        """Test scrape_books with no books found"""
        mock_html = """
        <html>
            <body>
                <div>No books found</div>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        result = scrape_books("https://example.com")
        
        assert result == []


class TestGetGenreSlugMap:
    """Test cases for get_genre_slug_map function"""
    
    @patch('scraper.books_scraper.fetch_page')
    def test_get_genre_slug_map(self, mock_fetch_page):
        """Test get_genre_slug_map returns correct mapping"""
        mock_html = """
        <html>
            <body>
                <ul class="nav-list">
                    <ul>
                        <li><a href="catalogue/category/books/travel_2/index.html">Travel</a></li>
                        <li><a href="catalogue/category/books/mystery_3/index.html">Mystery</a></li>
                        <li><a href="catalogue/category/books/historical-fiction_4/index.html">Historical Fiction</a></li>
                        <li><a href="catalogue/category/books/sequential-art_5/index.html">Sequential Art</a></li>
                    </ul>
                </ul>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        # Clear the cache to ensure fresh call
        get_genre_slug_map.cache_clear()
        
        result = get_genre_slug_map()
        
        mock_fetch_page.assert_called_once_with(BASE_URL)
        
        expected = {
            'travel': 'travel_2',
            'mystery': 'mystery_3',
            'historical fiction': 'historical-fiction_4',
            'sequential art': 'sequential-art_5'
        }
        
        assert result == expected
    
    @patch('scraper.books_scraper.fetch_page')
    def test_get_genre_slug_map_caching(self, mock_fetch_page):
        """Test that get_genre_slug_map uses caching"""
        mock_html = """
        <html>
            <body>
                <ul class="nav-list">
                    <ul>
                        <li><a href="catalogue/category/books/fiction_10/index.html">Fiction</a></li>
                    </ul>
                </ul>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        # Clear the cache first
        get_genre_slug_map.cache_clear()
        
        # Call twice
        result1 = get_genre_slug_map()
        result2 = get_genre_slug_map()
        
        # Should only fetch once due to caching
        mock_fetch_page.assert_called_once_with(BASE_URL)
        
        # Results should be identical
        assert result1 == result2
        assert result1 == {'fiction': 'fiction_10'}
    
    @patch('scraper.books_scraper.fetch_page')
    def test_get_genre_slug_map_empty_nav(self, mock_fetch_page):
        """Test get_genre_slug_map with empty navigation"""
        mock_html = """
        <html>
            <body>
                <ul class="nav-list">
                    <ul>
                    </ul>
                </ul>
            </body>
        </html>
        """
        mock_fetch_page.return_value = mock_html
        
        # Clear the cache to ensure fresh call
        get_genre_slug_map.cache_clear()
        
        result = get_genre_slug_map()
        
        assert result == {}


# Integration tests (these make actual HTTP requests)
class TestIntegration:
    """Integration tests that make real HTTP requests"""
    
    def test_fetch_page_real_request(self):
        """Test fetch_page with real HTTP request to books.toscrape.com"""
        html = fetch_page("https://books.toscrape.com/")
        
        # Check for DOCTYPE (case insensitive)
        assert html.lower().startswith("<!doctype html>")
        assert "<html" in html
        assert "</html" in html
        normalized = ' '.join(html.split())
        assert "All products | Books to Scrape - Sandbox" in normalized
    
    def test_get_genre_slug_map_real_request(self):
        """Test get_genre_slug_map with real HTTP request"""
        # Clear cache to ensure fresh request
        get_genre_slug_map.cache_clear()
        
        result = get_genre_slug_map()
        
        # Should have some genres
        assert len(result) > 0
        assert isinstance(result, dict)
        
        # Check that all values are strings and follow expected pattern
        for genre, slug in result.items():
            assert isinstance(genre, str)
            assert isinstance(slug, str)
            assert len(genre) > 0
