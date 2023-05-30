import os
import uuid
import threading
from typing import Tuple, Optional, List, Dict

from threading import Lock
from utils.log_config import logger
from crawlers.state import CrawlerState
from fake_useragent import UserAgent


file_write_lock = threading.Lock()


class BaseCrawler:
    def __init__(self, state: CrawlerState, timeout: int) -> None:
        self.state = state
        self.headers = self.get_random_headers()
        self.timeout = timeout
        self.lock = Lock()

    @staticmethod
    def get_random_headers() -> Dict[str, str]:
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {"User-Agent": user_agent}

    def crawl_page(self, thread_name: str, page_url: str) -> None:
        print(f"Crawling page_url: {page_url}")

        logger.info(thread_name + " is now crawling " + page_url)
        logger.info(
            "Queue "
            + str(self.state.crawl_queue.qsize())
            + " | Crawled  "
            + str(len(self.state.crawled_domains))
        )

        html_content, found_links = self.fetch_pages(page_url)

        if html_content is not None:
            # Save HTML before removing URL from the queue
            self.save_html_content(f"{uuid.uuid4()}.html", html_content)
        else:
            logger.debug(f"Not found html content for {page_url}")

        if found_links is not None:
            self.state.add_links_to_queue(found_links)
        else:
            logger.debug(f"Not found any link for {page_url}")

        # Protect the update with a lock
        with self.lock:
            self.state.crawled_domains.add(page_url)

    def save_html_content(self, page_url: str, html_content: str) -> None:
        # Generate a valid file name from the URL
        file_path = os.path.join(
            self.state.project_directory, self.state.project_name, page_url)

        # Write HTML content to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(html_content)

    def fetch_pages(self) -> Tuple[Optional[str], Optional[List[str]]]:
        raise NotImplementedError
