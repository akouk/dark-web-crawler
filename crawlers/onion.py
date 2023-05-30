import logging
import requests
from typing import Tuple, Optional, List, Dict

from utils.log_config import logger
from crawlers import base, state
from scrapper.page import PageScrapper


class OnionCrawler(base.BaseCrawler):
    def __init__(self, state: state.CrawlerState, proxies: Dict[str, str], timeout: int) -> None:
        super().__init__(state, timeout)
        self.proxies = proxies

    def get_tor_session(self) -> requests.Session:
        session = requests.session()
        session.proxies = self.proxies
        return session

    def fetch_pages(self, page_url: str) -> Tuple[Optional[str], Optional[List[str]]]:
        session = self.get_tor_session()
        logging.info("Getting url: " + page_url)

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
