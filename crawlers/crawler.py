import requests
from typing import Tuple, Optional, List

from utils.log_config import logger
from config_types import ConfigProxies
from crawlers.base import BaseCrawler
from scrappers.page import PageScrapper


class Crawler(BaseCrawler):

    def fetch_pages(self, page_url: str, proxies: Optional[ConfigProxies], thread_name: str) -> Tuple[Optional[str], Optional[List[str]]]:
        #logging.info("Getting url: " + page_url)

        try:
            response = requests.get(page_url, headers=self.headers, timeout=self.timeout, proxies=proxies)
            #logger.info(f"Status code: {response.status_code} from {thread_name}")
        
            if response.status_code == 200:
                logger.info(f"Request from {thread_name} went through successfully")

                # Set default encoding to "utf-8" if encoding is None
                html_content = response.text

                page_scrapper = PageScrapper(html_content)
                domains = page_scrapper.find_onion_links()
                logger.info(f"{thread_name} found {len(domains)} links on {page_url}")

                return html_content, [f"http://{address}" for address in domains]

        except requests.exceptions.ConnectionError as error:
            # Extract the error message from the exception
            # Log only the error message
            logger.error(f"Connection Error for domain: {page_url}. ERROR: {str(error)}")
            pass

        except requests.exceptions.ReadTimeout as error:
            logger.error(f"Read timeout for domain: {page_url}. ERROR: {str(error)}")
            pass

        except requests.exceptions.Timeout:
            logger.error(f"Timeout for domain: {page_url}. ERROR: {str(error)}")
            pass
        
        return None, None
