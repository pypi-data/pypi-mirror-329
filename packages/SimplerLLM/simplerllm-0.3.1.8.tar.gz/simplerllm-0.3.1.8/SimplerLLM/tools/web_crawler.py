import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def is_internal_url(url, base_url):
    parsed_url = urlparse(url)
    parsed_base_url = urlparse(base_url)
    return parsed_url.netloc == parsed_base_url.netloc

def crawl_website(url, depth, slug=None):
    visited_urls = set()
    results = {}

    def crawl_url(current_url, current_depth):
        if current_url in visited_urls:
            return
        visited_urls.add(current_url)

        try:
            response = requests.get(current_url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                links = soup.find_all('a', href=True)
                internal_links = []

                for link in links:
                    href = link.get('href')
                    absolute_url = urljoin(current_url, href)

                    if is_internal_url(absolute_url, url) and absolute_url not in visited_urls:
                        if not slug or slug in absolute_url:
                            internal_links.append(absolute_url)
                            crawl_url(absolute_url, current_depth + 1)

                results[current_url] = (internal_links, len(internal_links), set(internal_links))

        except Exception as e:
            return results

    crawl_url(url, 0)
    return results