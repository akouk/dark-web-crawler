import os
import uuid
from threading import Lock
from typing import Tuple, Optional, List, Dict

from fake_useragent import UserAgent

from utils.log_config import logger
from crawlers.state import CrawlerState
from config_types import ConfigProxies


class BaseCrawler:
    def __init__(self, state: CrawlerState, timeout: int, proxies: ConfigProxies) -> None:
        self.state = state
        self.headers = self.get_random_headers()
        self.timeout = timeout
        self.proxies = proxies
        self.lock = Lock()

    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {"User-Agent": user_agent}

    def crawl_page(self, thread_name: str, page_url: str) -> None:

        logger.info(f"{thread_name} is now crawling {page_url}")
        logger.info(f"Queue {str(self.state.crawl_queue.qsize())} | Crawled {str(len(self.state.crawled_domains))}")

        html_content, found_links = self.fetch_pages(page_url, self.proxies, thread_name)

        if ".onion" in page_url:
            if html_content is not None:
                # Save HTML before removing URL from the queue
                self.save_html_content(page_url.replace("http://", "").replace(".onion", "") + ".html", html_content)
                logger.info(f"The content of {page_url} is successfully saved")
            else:
                logger.info(f"{thread_name} did not found html content on {page_url}.")

        if found_links is not None:
            self.state.add_links_to_queue(found_links)


        # Protect the update with a lock
        with self.lock:
            self.state.crawled_domains.add(page_url)

    def save_html_content(self, page_url: str, html_content: str) -> None:
        # Generate a valid file name from the URL
        file_path = os.path.join(
            self.state.project_directory, self.state.project_name, page_url)

        try:
            # Write HTML content to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(html_content)
        except FileNotFoundError:
            pass
        except IOError as error:
            logger.info(f"An error occurred while writing the content of: {page_url}")
            logger.error(str(error))

    def fetch_pages(self, page_url:str, proxies: ConfigProxies) -> Tuple[Optional[str], Optional[List[str]]]:
        raise NotImplementedError()
