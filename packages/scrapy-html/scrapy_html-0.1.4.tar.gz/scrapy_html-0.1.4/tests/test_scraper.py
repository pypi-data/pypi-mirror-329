import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scrapy_html.scraper import get_html_content


def test_get_html_content():
    url = "https://httpbin.org/html"
    html = get_html_content(url)
    assert "<html>" in html and "</html>" in html
