import logging
import requests

import chardet

from utils.log_config import logger
from scrappers.page import PageScrapper
from crawlers.base import BaseCrawler


class PageCrawler(BaseCrawler):
    logger.debug("START OF PAGE CRAWLER")

    def fetch_pages(self, page_url):
        try:
            response = requests.get(page_url, headers=self.headers, timeout=30)
            logger.info(f"Status code: {response.status_code}")

            if response.status_code == 200:
                logging.info("Request went through. \n")

                encoding = chardet.detect(response.content)["encoding"]
                encoding = (
                    encoding or "utf-8"
                )  # Set default encoding to 'utf-8' if encoding is None

                html_content = response.content.decode(encoding)

                page_scrapper = PageScrapper(html_content)
                domains = page_scrapper.find_onion_links()

                return html_content, [f"http://{address}" for address in domains]

        except requests.exceptions.RequestException as e:
            logger.exception(
                "Exception occurred while trying to fetch %s. Exception: %s",
                page_url,
                str(e),
            )
            return []
