from fake_useragent import UserAgent
from file_manager import *
from log_config import logger

from threading import Lock


class BaseCrawler:
    def __init__(self, state):
        self.state = state
        self.headers = self.get_random_headers()

    @staticmethod
    def get_random_headers():
        user_agents_list = UserAgent()
        user_agent = user_agents_list.random
        return {"User-Agent": user_agent}

    lock = Lock()

    def crawl_page(self, thread_name, page_url):
        if page_url not in self.state.crawled_links.queue:
            logger.info(thread_name + " is now crawling " + page_url)
            logger.info(
                "Queue "
                + str(self.state.links_to_crawl.qsize())
                + " | Crawled  "
                + str(self.state.crawled_links.qsize())
            )
            self.state.add_links_to_queue(self.fetch_pages(page_url))
            with self.lock:  # Protect the update with a lock
                if page_url in self.state.links_to_crawl.queue:
                    self.state.links_to_crawl.queue.remove(page_url)
                    self.state.crawled_links.put(page_url)
            self.state.update_files()

    def fetch_pages(self):
        raise NotImplementedError
