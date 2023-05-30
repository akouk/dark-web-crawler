import logging
import requests
from typing import Tuple, Optional, List

from utils.log_config import logger
from scrapper.page import PageScrapper
from crawlers.base import BaseCrawler


class PageCrawler(BaseCrawler):
    def fetch_pages(self, page_url: str) -> Tuple[Optional[str], Optional[List[str]]]:
        try:
            response = requests.get(page_url, headers=self.headers, timeout=self.timeout)
            logger.info(f"Status code: {response.status_code}")

            if response.status_code == 200:
                logging.info("Request went through. \n")

                # Set default encoding to "utf-8" if encoding is None
                html_content = response.text

                page_scrapper = PageScrapper(html_content)
                domains = page_scrapper.find_onion_links()

                return html_content, [f"http://{address}" for address in domains]

        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass

        return None, None

