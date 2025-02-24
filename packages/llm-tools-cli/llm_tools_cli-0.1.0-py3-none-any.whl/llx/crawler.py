import requests
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

class Crawler:
    def __init__(self, start_url, domain=None, max_depth=1, max_urls=1):
        self.start_url = start_url
        self.domain = domain
        self.max_depth = max_depth
        self.max_urls = max_urls
        self.visited = set()

    def crawl(self):
        self._crawl_recursive(self.start_url, 0)
        return list(self.visited)

    def _crawl_recursive(self, url, depth):
        if depth > self.max_depth or url in self.visited or len(self.visited) >= self.max_urls:
            return
        try:
            response = requests.get(url)
            response.raise_for_status()
            self.visited.add(url)
        except requests.RequestException as e:
            return
        soup = BeautifulSoup(response.text, 'html.parser')
        for link in soup.find_all('a', href=True):
            next_url = urljoin(url, link['href'])
            if self._is_valid_url(next_url):
                self._crawl_recursive(next_url, depth + 1)

    def _is_valid_url(self, url):
        if self.domain:
            return urlparse(url).netloc == self.domain
        return True
