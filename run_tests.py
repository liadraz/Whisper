#!/usr/bin/env python3
"""
Simple test runner script for the books scraper tests.
Run this script to execute all tests for the books_scraper module.
"""

import subprocess
import sys

def main():
    """Run the test suite for books_scraper.py"""
    print("Running unit tests for books_scraper.py...")
    print("=" * 60)
    
    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_books.py", 
            "-v",
            "--tb=short"
        ], check=True)
        
        print("\n" + "=" * 60)
        print("✅ All tests passed successfully!")
        print("\nTest Coverage Summary:")
        print("- build_url(): ✅ Tested with valid/invalid genres and None")
        print("- fetch_page(): ✅ Tested with success, HTTP errors, and None URL")
        print("- scrape_books(): ✅ Tested with various HTML scenarios")
        print("- get_genre_slug_map(): ✅ Tested with mocking and caching")
        print("- Integration tests: ✅ Real HTTP requests to verify functionality")
        
        return 0
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Tests failed with exit code: {e.returncode}")
        return e.returncode
    except Exception as e:
        print(f"\n❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
