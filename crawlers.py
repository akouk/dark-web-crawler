from scraper import PageScrapper
import requests
import chardet
from file_manager import *
import logging
from BaseCrawler import BaseCrawler
from log_config import logger


class PageCrawler(BaseCrawler):
    logger.debug("START OF PAGE CRAWLER")

    def fetch_pages(self, page_url):
        try:
            response = requests.get(page_url, headers=self.headers, timeout=30)
            logger.info(f"Status code: {response.status_code}")
            logger.debug(
                f"Response text: {response.text[:100]}"
            )  # log only first 100 characters

            if response.status_code == 200:
                logging.info("Request went through. \n")
                html_content = response.content.decode("utf-8")
                page_scrapper = PageScrapper(html_content)
                onion_addresses = page_scrapper.find_onion_links()
                logger.info("Found unique onion addresses: %s", onion_addresses)
                page_scrapper.save_onion_addresses(
                    onion_addresses, self.state.links_to_crawl_file
                )
                return onion_addresses

        except requests.exceptions.RequestException as e:
            logger.exception(
                "Exception occurred while trying to fetch %s. Exception: %s",
                page_url,
                str(e),
            )
            return []


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
