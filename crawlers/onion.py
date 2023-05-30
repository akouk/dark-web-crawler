import chardet
import logging
import requests
from typing import Dict

from crawlers import base, state
from scrappers.page import PageScrapper


class OnionCrawler(base.BaseCrawler):
    def __init__(self, state: state.CrawlerState, proxies: Dict[str, str]):
        super().__init__(state)
        self.proxies = proxies

    def get_tor_session(self):
        session = requests.session()
        session.proxies = self.proxies
        return session

    def fetch_pages(self, page_url):
        session = self.get_tor_session()
        logging.info("Getting url: " + page_url)

        try:
            response = session.get(page_url, headers=self.headers, timeout=30)
            response.raise_for_status()  # Raise exception if request was not successful
            logging.info("Request went through.\n")

            # Detect character encoding using chardet
            encoding = chardet.detect(response.content)["encoding"]
            encoding = (
                encoding or "utf-8"
            )  # Set default encoding to 'utf-8' if encoding is None
            html_content = response.content.decode(encoding)

            # Extract onion links
            page_scrapper = PageScrapper(html_content)
            domains = page_scrapper.find_onion_links()

            return html_content, [f"http://{address}" for address in domains]

        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error for {page_url}: {e}")
            return []

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return []
