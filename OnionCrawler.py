from PageScrapper import PageScrapper
import requests
import chardet
from file_manager import *
import logging
from BaseCrawler import BaseCrawler
from log_config import logger

class OnionCrawler(BaseCrawler):
    def __init__(self, state, proxies):
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
            return page_scrapper.find_onion_links()

        except requests.exceptions.ConnectionError as e:
            logging.error(f"Connection error for {page_url}: {e}")
            return None
        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error occurred: {e}")
            return None
